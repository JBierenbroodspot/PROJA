import datetime
import os
import urllib.parse
from typing import Any, Union

import django.views
import requests
from TwitterAPI import TwitterAPI, TwitterResponse
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware

from ns_zuil import models, forms


class MessageView(django.views.generic.edit.FormView):
    """A FormView that overwrites form_valid to create models.Message object.
    """
    template_name = "message_form.html"
    form_class = forms.MessageForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inserts a models.Station instance with the same id that has been provided in the url using self.kwargs
        into the context dictionary. This way the template provided by self.template_name can access the information
        within the Station object.

        Returns:
            A dictionary containing all context data that has been inherited from the parent class together with the
            new information from the models.Station object.
        """
        # Super calls executes the function that is called.
        context: dict[Any] = super(MessageView, self).get_context_data(**kwargs)
        # When a the url is defined like <int:station_id> the value will be stored in self.kwargs.
        context["station"] = models.Station.objects.get(id=int(self.kwargs["station_id"]))
        return context

    def form_valid(self, form: forms.MessageForm) -> HttpResponseRedirect:
        """Converts data supplied by form into a dictionary using clean(form). The cleaned data will be passed to
        self.create_message and finally self.success_url will be set to return user to the same page containing a clean
        form.

        Args:
            form: A forms.MessageForm instance with it's datafields filled. This argument is passed by the class' post()
            method.

        Returns:
            A super call to parent form_valid which will return a redirect to self.success_url.
        """
        cleaned: dict[Any] = self.clean(form)
        self.create_message(cleaned)

        # Retrieves url of the current page.
        self.success_url = self.request.path_info
        return super().form_valid(form)

    def create_message(self, data: dict[Any]) -> None:
        """Creates a models.Message instance using the dictionary data. The only key that is not optional in data is
        data["message"].

        Args:
            data:A dictionary containing the keys (message, firtsname, insertion, lastname).

        Returns:
            None.
        """
        # Author note: This method should actually catch exceptions but it is very hard to find all possible errors
        # that can be thrown. Furthermore is the process relatively safe because the form cannot post data that is not
        # handleable by the database. If exceptions can be caught however, this method could actually return a
        # meaningful value measuring whether the database insert was successful or not.
        models.Message(message=data["message"],
                       firstname=data["firstname"],
                       insertion=data["insertion"],
                       lastname=data["lastname"],
                       station_fk_id=self.get_context_data()["station"].id
                       ).save()

    @staticmethod
    def clean(form: forms.MessageForm) -> dict[Any]:
        """Cleans data provided by a messageForm using form.cleaned_data and then makes sure firstname and lastname are
        not null. If they are a default value will be supplied.

        Returns:
            A dictionary containing containing form data.
        """
        cleaned: dict[Any] = form.cleaned_data
        if cleaned["firstname"] == "" and cleaned["lastname"] == "":
            cleaned["firstname"] = "A."
            cleaned["lastname"] = "Noniem"
        return cleaned


class ChooseStationView(django.views.generic.edit.FormView):
    """A FormView that displays all Station instances in a form.
    """
    # Author note: This feature is for development purposes only and should be removed from a production environment.
    template_name = "select_station_form.html"
    form_class = forms.StationForm

    def form_valid(self, form: forms.StationForm) -> HttpResponseRedirect:
        """Gets the primary key of the Station instance provided by the form, which has been cleaned using
        cleaned_data. Then it sets the success_url to that primary key.

        Returns:
            A super call to parent form_valid which returns a redirect to success_url.
        """
        cleaned: dict[Any] = form.cleaned_data
        self.success_url = str(cleaned["station"].pk)
        return super().form_valid(form)


# Adds login required decorator to the dispatch method of this class.
# This way you always need to be logged in for this class.
@method_decorator(login_required, name="dispatch")
class ModeratorView(django.views.generic.edit.FormView):
    """A FormView for modifying a Message object with data gathered from a ModerationForm.
    """
    message: models.Message = None

    template_name = "moderation_form.html"
    form_class = forms.ModerationForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inserts the first models.Message instance with the status == PENDING into the context dictionary. This way
        the template provided by self.template_name can access the information within the Message object.

        Returns:
            A dictionary containing all context data that has been inherited from the parent class together with the
            new information from the models.Message object.
        """
        context: dict[str, Any] = super(ModeratorView, self).get_context_data(**kwargs)
        context["message"] = models.Message.objects.filter(status="PENDING").first()
        return context

    def form_valid(self, form: forms.ModerationForm) -> HttpResponseRedirect:
        """Converts data supplied by form into a dictionary using cleaned_data. The cleaned data will be passed to
        self.update_message and finally self.success_url will be set to return user to the same page containing a clean
        form.

        Args:
            form: A forms.ModerationForm instance with it's datafields filled. This argument is passed by the
            class' post() method.

        Returns:
            A super call to parent form_valid which will return a redirect to self.success_url.
        """
        self.message = self.get_context_data()["message"]
        cleaned: dict[Any] = form.cleaned_data
        self.update_message(cleaned)
        if self.message.status == "ACCEPTED":
            self.tweet_message()
        self.success_url = self.request.path_info
        return super().form_valid(form)

    def update_message(self, data: dict[Any]) -> None:
        """Updates a models.Message instance using the dictionary data together with the current time and current user.

        Args:
            data: A dictionary containing the key status.

        Returns:
            None.
        """
        # Author note: See author note MessageView.create_message.
        self.message.status = data["status"]
        # make_aware makes the datetime instance aware of what timezone it is.
        self.message.moderation_datetime = make_aware(datetime.datetime.now())
        self.message.moderated_by_fk = self.request.user
        self.message.save()

    def build_tweet(self) -> str:
        """Uses self.message to build message which can be tweeted.

        Returns:
            String in the format of: '[fullname] op [station] zegt: [message].
        """
        tweet: str = f"{self.message.fullname} op {self.message.station_fk} zegt:\n{self.message.message}"
        if len(tweet) > 280:
            tweet = tweet[:279]
        return tweet

    def tweet_message(self) -> int:
        """Uses the TwitterAPI together with keys taken from .env file. A message will be built using
        self.build_tweet and is used as a parameter for a request to the statuses/update resource.

        Returns:
            The statuscode of the request.
        """
        api: TwitterAPI = TwitterAPI(os.getenv("TWITTER_API"),
                                     os.getenv("TWITTER_SECRET"),
                                     os.getenv("TWITTER_ACCESS_TOKEN"),
                                     os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
        response: TwitterResponse = api.request("statuses/update", {"status": self.build_tweet()})
        return response.status_code


@method_decorator(login_required, name="dispatch")
class DeniedView(django.views.generic.ListView):
    """A ListView that gets all models.Message instances with the status DENIED and makes them available for the
    template defined in template_name.
    """
    model = models.Message
    queryset = models.Message.objects.filter(status="DENIED")
    template_name = "denied_messages_list.html"


class DisplayView(django.views.generic.ListView):
    """A ListView for displaying up to 10 of the most recent messages. The messages are retrieved by the station_id from
    url.
    """
    model = models.Message
    template_name = "display_list.html"

    def get_queryset(self) -> QuerySet:
        """Gets a QuerySet of a Message model filtered on timedelta between now and DISPLAY_INTERVAL in .env file. Then
        filtered on on station and ordered descending.

        Returns:
            QuerySet with models.Message instances added between now and the now - DISPLAY_INTERVAL where the
            station_fk_id is the same as station_id in the url, ordered descending.
        """
        now: datetime.datetime = make_aware(datetime.datetime.now())
        queryset: QuerySet = self.model.objects.filter(
            moderation_datetime__range=[now - datetime.timedelta(hours=float(os.getenv("DISPLAY_INTERVAL"))), now],
            station_fk_id=self.kwargs["station_id"]
        ).order_by("-post_datetime")[:10]  # The - in front of the field name means that it is ordered descending.
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gets station from from get_station() and weather from get_weather_info() and inserts it into the context
        dictionary. This way the template provided by self.template_name can access the information within the Message
        object.

        Returns:
            A dictionary containing all context data that has been inherited from the parent class together with
            the gathered from the url using self.kwargs and weather info for the city provided by the models.Station
            instance.
        """
        context: dict[str, Any] = super(DisplayView, self).get_context_data(**kwargs)
        context["station"] = self.get_station()
        context["weather"] = self.get_weather_info()
        return context

    def get_weather_info(self) -> dict[str, Any]:
        """Gets weather info from openweathermap api by retrieving the api key from a .env file. A request will be
        sent with the city field from a models.Station object as a parameter.

        Returns:
            A dictionary containing the weather information in json format.
        """
        api_key: str = os.getenv('WEATHER_API_KEY')
        url: str = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={api_key}"
        city: str = self.get_station().city
        weather: dict[str, Any] = requests.get(url.format(city)).json()
        return weather

    def get_station(self) -> QuerySet:
        """Gets a models.Station instance with the same id provided by the url using self.kwargs.

        Returns:
            QuerySet containing a models.Station instance.
        """
        station: QuerySet = models.Station.objects.get(id=self.kwargs["station_id"])
        return station


class TweetView(django.views.generic.TemplateView):
    """A TemplateView that utilizes the TwitterAPI to display up to 10 of the mose recent Tweets tweeted by
    ModeratorView on the template defined in self.template_name.
    """
    template_name = "display_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gets station from from get_station(), weather from get_weather_info() and tweets in the form of html code.
        These are inserted into the context dictionary. This way the template provided by self.template_name can
        access the information within the Message object.

        Returns:
            A dictionary containing all context data that has been inherited from the parent class together with
            the gathered from the url using self.kwargs, weather info for the city provided by the models.Station
            instance and html-ready tweets.
        """
        context: dict[str, Any] = super(TweetView, self).get_context_data(**kwargs)
        context["station"] = self.get_station()
        context["tweets"] = self.get_tweets()
        context["weather"] = self.get_weather_info()
        return context

    def get_weather_info(self) -> dict[str, Any]:
        """Gets weather info from openweathermap api by retrieving the api key from a .env file. A request will be
        sent with the city field from a models.Station object as a parameter.

        Returns:
            A dictionary containing the weather information in json format.
        """
        api_key: str = os.getenv('WEATHER_API_KEY')
        url: str = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={api_key}"
        city: str = self.get_station().city
        weather: dict[str, Any] = requests.get(url.format(city)).json()
        return weather

    def get_station(self) -> QuerySet:
        """Gets a models.Station instance with the same id provided by the url using self.kwargs.

        Returns:
            QuerySet containing a models.Station instance.
        """
        station: QuerySet = models.Station.objects.get(id=self.kwargs["station_id"])
        return station

    def get_tweets(self) -> list[str]:
        """Initializes a v2 TwitterAPI to retrieve tweet id's from TWITTER_USER defined in .env. A url will be built
        using these tweet id's. These tweets will be passed to self.get_html_from_twitter_status and a list
        containing html for every tweet will be returned.

        Returns: A list containing html code of tweets posted by a specific user in a specific time range and an
        empty list if there are no tweets.
        """
        tweets: list[str] = []
        api: TwitterAPI = TwitterAPI(os.getenv("TWITTER_API"),
                                     os.getenv("TWITTER_SECRET"),
                                     os.getenv("TWITTER_ACCESS_TOKEN"),
                                     os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                                     api_version="2")
        # Gets a timezone aware version of datetime.now.
        now: datetime.datetime = make_aware(datetime.datetime.now())
        # Subtracts now - DISPLAY_INTERVAL from now.
        start_time: datetime.datetime = now - datetime.timedelta(hours=float(os.getenv("DISPLAY_INTERVAL")))
        # Removes microseconds because they are not supported by Twitter.
        start_time = start_time.replace(microsecond=0)
        # Data dictionary will be passed as a parameter.
        data: dict[str, Any] = {
            "start_time": start_time.isoformat(),
            "tweet.fields": ["created_at"],
        }
        user_id: str = os.getenv("TWITTER_USER")
        # This will send a request to the users/:id/tweets resource of the Twitter API and it will return a list of the
        # id's of tweets posted by this user.
        status: dict[str, Any] = api.request(f"users/:{user_id}/tweets", data).json()
        if "data" in status:
            tweets = self.get_html_from_twitter_status(status["data"])
        elif "errors" in status:
            tweets = status["errors"]
        return tweets

    @staticmethod
    def get_html_from_twitter_status(status: dict[str, Any]) -> list[str]:
        """Takes the id's out of a TwitterResponse containing a status and sends a request to publish.twitter's
        oembed resource with a link to the tweet for every tweet in the status. Then it will filter for the html code
        and adds it to a list.

        Args:
            status: A TwitterResponse object containing a list of statuses and their id's.

        Returns:
            A list containing html-code which can be directly pasted into a template.
        """
        html: list[str] = []
        for tweet in status:
            # urllib.parse.quote here turns the link into url-safe syntax. The save argument '/' by default,
            # by setting this to '' slashes will also be turned into url-save syntax. The 'user' part in the url
            # should be the twitter handle of the person who tweeted the tweet but the oembed api automatically
            # corrects it based on the tweet id.
            tweet_url: str = urllib.parse.quote(f"https://twitter.com/user/status/{tweet['id']}", safe="")
            # Sends a request using requests to the publis.twitter oembed resource. This will return some metadata
            # and html code to build the tweet. With the 'dnt' parameter set to true Twitter will not use this
            # timeline for personalized ad purposes.
            embed_tweet = requests.get(f"https://publish.twitter.com/oembed?url={tweet_url}&dnt=true")
            if embed_tweet.status_code == 200:
                html.append(embed_tweet.json()["html"])
        return html
