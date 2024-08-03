from django.db import models


class WeatherRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    city1 = models.CharField(max_length=100)
    city2 = models.CharField(max_length=100)