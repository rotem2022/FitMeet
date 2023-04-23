from django.db import models
from django.db.utils import IntegrityError


class Teams(models.Model):
    name = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        all_teams = Teams.objects.all()
        teams_names = [team.name for team in all_teams]
        if self.name in teams_names:
            raise IntegrityError
        super().save(*args, **kwargs)
