from django import forms

from ns_zuil import models


class StationForm(forms.Form):
    station = forms.ModelChoiceField(queryset=models.Station.objects.all())


class MessageForm(forms.Form):
    message: forms.CharField = forms.CharField(max_length=140, widget=forms.Textarea(attrs={"rows": 4}))
    firstname: forms.CharField = forms.CharField(max_length=30, required=False)
    insertion: forms.CharField = forms.CharField(max_length=15, required=False)
    lastname: forms.CharField = forms.CharField(max_length=30, required=False)


class ModerationForm(forms.Form):
    status: forms.ChoiceField = forms.ChoiceField(choices=(
        ("ACCEPTED", "Accepteren"),
        ("DENIED", "Weigeren"),
    ))
    comment: forms.CharField = forms.CharField(max_length=255, required=False)
