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
    """A FormView for inserting form data from a MessageForm into a Message model.
    """
    template_name = "message_form.html"
    form_class = forms.MessageForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Inserts a Station object with corresponding ID from url into the context dict.

        Returns:
            Context dict with a Station object inserted.
        """
        context: dict[Any] = super(MessageView, self).get_context_data(**kwargs)
        context["station"] = models.Station.objects.get(id=int(self.kwargs["station_id"]))
        return context

    def form_valid(self, form: forms.MessageForm) -> HttpResponseRedirect:
        """Creates and saves a Message object.

        Args:
            form: A MessageForm containing information for creating a Message object.

        Returns:
            Redirect to the same url with a clean form.
        """
        cleaned: dict[Any] = self.clean(form)
        self.success_url = self.request.path_info  # Get current url
        models.Message(message=cleaned["message"],
                       firstname=cleaned["firstname"],
                       insertion=cleaned["insertion"],
                       lastname=cleaned["lastname"],
                       station_fk_id=self.get_context_data()["station"].id
                       ).save()
        return super().form_valid(form)

    @staticmethod
    def clean(form: forms.MessageForm) -> dict[Any]:
        """Cleans a MessageForm using cleaned_data. Changes empty first and lastname fields into the their defaults.

        Returns:
            Dict containing clean an non-empty data.
        """
        cleaned: dict[Any] = form.cleaned_data
        if cleaned["firstname"] == "" and cleaned["lastname"] == "":
            cleaned["firstname"] = "A."
            cleaned["lastname"] = "Noniem"
        return cleaned


class ChooseStationView(django.views.generic.edit.FormView):
    """A FormView for redirecting to a page associated with a Station object.

    This feature is for development purposes only and should be removed from a production environment.
    """
    template_name = "select_station_form.html"
    form_class = forms.StationForm

    def form_valid(self, form: forms.StationForm) -> HttpResponseRedirect:
        """Redirects to page selected in a StationForm.

        Returns:
            Redirect to page selected in the form.
        """
        cleaned: dict[Any] = form.cleaned_data
        # TODO(Jbierenbroodspot): Find out what this does and if it's necessary.
        self.get_context_data()["station_id"] = cleaned["station"].pk
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
        message: models.Message = self.get_context_data()["message"]
        message.status = cleaned["status"]
        message.moderation_datetime = make_aware(datetime.datetime.now())
        message.moderated_by_fk = self.request.user
        message.save()
        self.success_url = self.request.path_info
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DeniedView(django.views.generic.ListView):
    model = models.Message
    queryset = models.Message.objects.filter(status="DENIED")
    template_name = "denied_messages_list.html"


class DisplayView(django.views.generic.ListView):
    model = models.Message
    template_name = "display_list.html"

    def get_queryset(self) -> QuerySet:
        now: datetime.datetime = make_aware(datetime.datetime.now())
        queryset: QuerySet = self.model.objects.filter(
            moderation_datetime__range=[now - datetime.timedelta(hours=int(os.getenv("DISPLAY_INTERVAL"))), now],
            station_fk_id=self.kwargs["station_id"]
        )
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super(DisplayView, self).get_context_data(**kwargs)
        context["station"] = self.get_station()
        context["weather"] = self.get_weather_info()
        return context

    def get_weather_info(self) -> dict[str, Any]:
        url: str = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&appid={os.getenv('WEATHER_API_KEY')}"
        city: str = self.get_station().city
        weather: dict[str, Any] = requests.get(url.format(city)).json()
        return weather

    def get_station(self):
        station: QuerySet = models.Station.objects.get(id=self.kwargs["station_id"])
        return station

