from django.db import migrations, transaction


def create_initial_events(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')
    Event = apps.get_model('event', 'Event')

    user_event = [
        ('Ofek', 2),
        ('Danny', 1),
        ('Rotem', 1),
        ('Saar', 1),
        ('Tal', 1),
        ('Rimon', 2),

    ]
    with transaction.atomic():
        for username, event_id in user_event:
            user = User.objects.filter(username=username).first()
            profile = Profile.objects.filter(user=user).first()
            Event.manager.join_event(user_id=profile.pk, event_id=event_id)


class Migration(migrations.Migration):
    dependencies = [
        ('category_location', '0002_static_data'),
        ('category', '0002_static_data'),
        ('location', '0002_static_data'),
        ('users', '0002_static_data'),
        ('event', '0005_alter_event_managers'),
        ('event', '0006_static_data'),
        ('poll', '0003_alter_poll_event_id')
    ]

    operations = [
        migrations.RunPython(create_initial_events),
    ]
