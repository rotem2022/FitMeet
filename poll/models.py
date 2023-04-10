from django.db import models
from django.utils import timezone
from datetime import timedelta


class Poll(models.Model):
    max_suggestions = models.PositiveIntegerField()
    end_time = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=2))
