import datetime
from typing import Any

import django.views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from ns_zuil import models, forms


class MessageView(django.views.generic.edit.FormView):
    template_name = "message_form.html"
    form_class = forms.MessageForm

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context["station"] = models.Station.objects.get(id=int(self.kwargs["station_id"]))
        return context

    def form_valid(self, form):
        cleaned: dict[Any] = form.cleaned_data
        if cleaned["firstname"] == "" and cleaned["lastname"] == "":
            cleaned["firstname"] = "A."
            cleaned["lastname"] = "Noniem"
        message = models.Message(message=cleaned["message"],
                                 firstname=cleaned["firstname"],
                                 insertion=cleaned["insertion"],
                                 lastname=cleaned["lastname"],
                                 station_fk_id=self.get_context_data()["station"].id)
        message.save()
        self.success_url = self.request.path_info
        return super().form_valid(form)


class ChooseStationView(django.views.generic.edit.FormView):
    template_name = "select_station_form.html"
    form_class = forms.StationForm

    def form_valid(self, form):
        cleaned: dict[Any] = form.cleaned_data
        self.get_context_data()["station_id"] = cleaned["station"].pk
        self.success_url = str(cleaned["station"].pk)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ModeratorView(django.views.generic.edit.FormView):
    template_name = "moderation_form.html"
    form_class = forms.ModerationForm

    def get_context_data(self, **kwargs):
        context = super(ModeratorView, self).get_context_data(**kwargs)
        context["message"] = models.Message.objects.filter(status="PENDING").first()
        return context

    def form_valid(self, form):
        cleaned = form.cleaned_data
        message = self.get_context_data()["message"]
        message.status = cleaned["status"]
        message.moderation_datetime = datetime.datetime.now()
        message.moderated_by_fk = self.request.user
        message.save()
        self.success_url = self.request.path_info
        return super().form_valid(form)
