from django.db import migrations, transaction
from django.utils import timezone
from datetime import timedelta


def create_initial_events(apps, schema_editor):
    Location = apps.get_model('location', 'Location')
    Category = apps.get_model('category', 'Category')
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')
    Event = apps.get_model('event', 'Event')

    soccer = Category.objects.filter(name="Soccer").first()
    basketball = Category.objects.filter(name='Basketball').first()
    bloomfield = Location.objects.filter(name="Bloomfield").first()
    holmes_place_family_a = Location.objects.filter(name='Holmes Place Family A').first()

    user_danny = User.objects.filter(username='Danny').first()
    profile_danny = Profile.objects.filter(user=user_danny).first()
    user_ofek = User.objects.filter(username='Ofek').first()
    profile_ofek = Profile.objects.filter(user=user_ofek).first()

    event_start_time = timezone.now() + timedelta(days=2)
    poll_end_time = timezone.now() + timedelta(days=1)
    event_end_time = timezone.now() + timedelta(days=3)

    event_data = [
        (soccer, bloomfield, '3 soccer games for fun', 10, event_start_time, event_end_time, False, poll_end_time,
         5, profile_ofek),
        (basketball, holmes_place_family_a, 'quick basketball game', 20, event_start_time, event_end_time,
         False, poll_end_time, 5, profile_danny)
    ]

    manager = Event.manager
    with transaction.atomic():
        for cat, loc, name, max_part, event_start, event_end, is_private, poll_end_time, poll_suggestions, user_id in \
                event_data:
            manager.create_event(category_id=cat.id, location_id=loc.id, name=name,
                                 max_participants=max_part, start_time=event_start,
                                 end_time=event_end,
                                 is_private=is_private, poll_end_time=poll_end_time,
                                 poll_suggestions=poll_suggestions, user_id=user_id.id)


class Migration(migrations.Migration):
    dependencies = [
        ('category_location', '0002_static_data'),
        ('category', '0002_static_data'),
        ('location', '0002_static_data'),
        ('users', '0002_static_data'),
        ('event', '0005_alter_event_managers'),
        ('poll', '0003_alter_poll_event_id')
    ]

    operations = [
        migrations.RunPython(create_initial_events),
    ]
