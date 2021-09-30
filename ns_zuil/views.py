from typing import Any

import django.views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from ns_zuil import models, forms


class MessageView(django.views.generic.edit.FormView):
    template_name = "write_message.html"
    form_class = forms.MessageForm
    success_url = "station"

    def form_valid(self, form):
        cleaned: dict[Any] = form.cleaned_data
        message = models.Message(message=cleaned["message"],
                                 firstname=cleaned["firstname"],
                                 insertion=cleaned["insertion"],
                                 lastname=cleaned["lastname"],
                                 station_fk_id=int(self.request.session.get("station_id")))
        message.save()
        return super().form_valid(form)


class ChooseStationView(django.views.generic.edit.FormView):
    template_name = "select_station.html"
    form_class = forms.StationForm
    success_url = "station/"

    def form_valid(self, form):
        cleaned: dict[Any] = form.cleaned_data
        self.request.session["station_id"] = cleaned["station"].pk
        self.success_url += str(cleaned["station"].pk)
        return super().form_valid(form)


# @login_required
class ModeratorView(django.views.generic.edit.FormView):
    template_name = "moderation_form.html"
    form_class = forms.ModerationForm
    success_url = "moderate"

    def form_valid(self, form):
        return super().form_valid(form)

