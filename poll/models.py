from django.db import models
from datetime import timedelta
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime


def get_default_end_date():
    return timezone.now() + timedelta(days=1)


class Poll(models.Model):
    event_id = models.OneToOneField(to='event.Event', on_delete=models.CASCADE,
                                    related_name='poll_ref', null=True,
                                    blank=True)
    max_suggestions = models.PositiveIntegerField()
    end_time = models.DateTimeField(default=get_default_end_date)

    invalid_poll_error = "The poll end time should be before the event start time."

    @staticmethod
    def create_poll(event, max_suggestions, end_time):
        Poll.verify_poll_end_time(event_start_time=event.start_time, poll_end_time=end_time)
        poll = Poll(event_id=event, max_suggestions=max_suggestions, end_time=end_time)
        poll.save()
        return poll

    @staticmethod
    def verify_poll_end_time(event_start_time, poll_end_time):
        if poll_end_time >= event_start_time:
            raise ValidationError(Poll.invalid_poll_error)

    def is_active(self):
        now = localtime().replace(tzinfo=None)
        end_time = localtime(self.end_time).replace(tzinfo=None)
        return now < end_time

    def show_suggestions(self):
        poll_suggestion_model = apps.get_model('poll_suggestion', 'PollSuggestion')
        return poll_suggestion_model.objects.filter(poll_id=self)

    def close_poll(self):
        self.end_time = timezone.now()
        self.save()

    def time_remaining(self):
        remaining = self.end_time.replace(tzinfo=None) - timezone.localtime().replace(tzinfo=None)
        if remaining < timedelta():
            return timedelta()
        return remaining
