from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    street_number = models.PositiveIntegerField()
    indoor = models.BooleanField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
