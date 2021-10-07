from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    message: models.CharField = models.CharField(max_length=140)
    firstname: models.CharField = models.CharField(max_length=255, default="A.")
    insertion: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    lastname: models.CharField = models.CharField(max_length=255, default="Noniem")
    post_datetime: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Posted on")
    status: models.CharField = models.CharField(max_length=20, default="PENDING")
    moderation_datetime: models.DateTimeField = models.DateTimeField(blank=True, null=True, verbose_name="Moderated on")
    station_fk: models.ForeignKey = models.ForeignKey("Station", on_delete=models.CASCADE, verbose_name="Station")
    moderated_by_fk: models.ForeignKey = models.ForeignKey(User,
                                                           on_delete=models.SET_NULL,
                                                           blank=True,
                                                           null=True,
                                                           verbose_name="Moderated by")

    def __str__(self):
        return f"Message {self.id}"

    @property
    def fullname(self):
        if self.insertion:
            return " ".join(map(str, [self.firstname, self.insertion, self.lastname]))
        else:
            return " ".join(map(str, [self.firstname, self.lastname]))


class Station(models.Model):
    name: models.CharField = models.CharField(max_length=255, unique=True)
    city: models.CharField = models.CharField(max_length=255)

    def __str__(self):
        return f"Station {self.name}"
