from django.db import models

from category.models import Category
from location.models import Location


class CategoryLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
