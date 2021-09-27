import django.views
from django.http import HttpResponse
from django.shortcuts import render


class MessageView(django.views.View):
    TEMPLATE = r""

    def get(self, request: object, *args, **kwargs) -> HttpResponse:
        context: dict[object] = {}
        return render(request, self.TEMPLATE, context)


class ModeratorView(django.views.View):
    TEMPLATE = r""

    def get(self, request: object, *args, **kwargs) -> HttpResponse:
        context: dict[object] = {}
        return render(request, self.TEMPLATE, context)