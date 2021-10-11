import datetime
import os
from typing import Any

import django.views
import requests
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
            function.

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

        Author note: This method should actually catch exceptions but it is very hard to find all possible errors
        that can be thrown. Furthermore is the process relatively safe because the form cannot post data that is not
        handleable by the database. If exceptions can be caught however, this method could actually return a
        meaningful value measuring whether the database insert was successful or not.
        """
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

    Author note:
        This feature is for development purposes only and should be removed from a production environment.
    """
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
    template_name = "moderation_form.html"
    form_class = forms.ModerationForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inserts the first Message object with the status PENDING into the context dict.

        Returns:
            Context dict containing a Message object.
        """
        context: dict[str, Any] = super(ModeratorView, self).get_context_data(**kwargs)
        context["message"] = models.Message.objects.filter(status="PENDING").first()
        return context

    def form_valid(self, form: forms.ModerationForm) -> HttpResponseRedirect:
        """Updates and saves a Message object.

        Args:
            form: A ModerationForm containing information about the status for an Message object.

        Returns:
            Redirect to the same url with a clean form.
        """
        cleaned: dict[Any] = form.cleaned_data
        self.update_message(cleaned)
        self.success_url = self.request.path_info
        return super().form_valid(form)

    def update_message(self, data: dict[Any]) -> None:
        """Updates Message model gathered from form data.

        Args:
            data: Dictionary containg form data needed to update mMessage model

        Returns:
            None
        """
        message: models.Message = self.get_context_data()["message"]
        message.status = data["status"]
        message.moderation_datetime = make_aware(datetime.datetime.now())
        message.moderated_by_fk = self.request.user
        message.save()


@method_decorator(login_required, name="dispatch")
class DeniedView(django.views.generic.ListView):
    """A ListView for displaying messages that have the status denied.
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
            QuerySet with applied filters.
        """
        now: datetime.datetime = make_aware(datetime.datetime.now())
        queryset: QuerySet = self.model.objects.filter(
            moderation_datetime__range=[now - datetime.timedelta(hours=int(os.getenv("DISPLAY_INTERVAL"))), now],
            station_fk_id=self.kwargs["station_id"]
        ).order_by("-post_datetime")[:10]
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gets station from from get_station() and weather from get_weather_info() and adds it to the context dict.

        Returns:
            Context dict containing weather and station.
        """
        context: dict[str, Any] = super(DisplayView, self).get_context_data(**kwargs)
        context["station"] = self.get_station()
        context["weather"] = self.get_weather_info()
        return context

    def get_weather_info(self) -> dict[str, Any]:
        """Gets weather info from openweathermap api using information stored in .env file.

        Returns:
            Weather information in json format.
        """
        url: str = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={os.getenv('WEATHER_API_KEY')}"
        city: str = self.get_station().city
        weather: dict[str, Any] = requests.get(url.format(city)).json()
        return weather

    def get_station(self) -> QuerySet:
        """Gets station by getting station_id from the object instance's class.

        Returns:
            QuerySet containing the station with corresponding id.
        """
        station: QuerySet = models.Station.objects.get(id=self.kwargs["station_id"])
        return station
