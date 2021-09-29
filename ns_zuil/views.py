from typing import overload, Any

import django.views
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ns_zuil import models, forms


class MessageView(django.views.generic.edit.FormView):
    template_name = "write_message.html"
    form_class = forms.MessageForm
    success_url = "#"

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


class ModeratorView(django.views.View):
    TEMPLATE = r""

    def get(self, request: Any, *args, **kwargs) -> HttpResponse:
        context: dict[Any] = {}
        return render(request, self.TEMPLATE, context)
