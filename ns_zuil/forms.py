from django import forms

from ns_zuil import models


class StationForm(forms.Form):
    station = forms.ModelChoiceField(queryset=models.Station.objects.all())


class MessageForm(forms.Form):
    message = forms.CharField(max_length=140)
    firstname = forms.CharField(max_length=255, required=False)
    insertion = forms.CharField(max_length=255, required=False)
    lastname = forms.CharField(max_length=255, required=False)