from django.db import models
from django.utils import timezone


class Measurement(models.Model):
    sensor = models.CharField(max_length=200)
    value = models.FloatField()
    created_date = models.DateTimeField(
            default=timezone.now)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.sensor
