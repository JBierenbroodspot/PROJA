from django.contrib import admin

from ns_zuil import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ("post_datetime",)


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    pass
