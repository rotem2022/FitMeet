from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Teams
import pytest

TEAM1 = 'Team 1'
LONG_NAME = 'A' * 32
EMPTY_NAME = ''


@pytest.mark.django_db
class TestTeamsModel:
    @pytest.mark.parametrize(
        "invalid_name",
        [EMPTY_NAME, LONG_NAME],
    )
    def test_create_team_with_invalid_name(self, invalid_name):
        with pytest.raises(ValidationError):
            Teams.objects.create(name=LONG_NAME).full_clean()

    def test_create_team_with_taken_name(self):
        Teams.objects.create(name=TEAM1)
        with pytest.raises(IntegrityError):
            Teams.objects.create(name=TEAM1)

    def test_save(self):
        team1 = Teams(name=TEAM1)
        team1.save()
        assert team1 in Teams.objects.all()
