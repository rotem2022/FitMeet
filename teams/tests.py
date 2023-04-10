from .models import Teams
import pytest


@pytest.fixture
def create_team():
    team = Teams.objects.create(name='Test Team')
    return team


@pytest.mark.django_db
class TestTeamsModel:

    def test_create_team(self, create_team):
        create_team.save()
        assert create_team in Teams.objects.all()

    def test_delete_team(self, create_team):
        create_team.save()
        create_team.delete()
        assert create_team not in Teams.objects.all()
