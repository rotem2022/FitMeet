from django.db import migrations, transaction


def create_initial_events(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')
    Event = apps.get_model('event', 'Event')

    user_danny = User.objects.filter(username='Danny').first()
    profile_danny = Profile.objects.filter(user=user_danny).first()
    user_ofek = User.objects.filter(username='Ofek').first()
    profile_ofek = Profile.objects.filter(user=user_ofek).first()
    user_rotem = User.objects.filter(username='Rotem').first()
    profile_rotem = Profile.objects.filter(user=user_rotem).first()
    user_saar = User.objects.filter(username='Saar').first()
    profile_saar = Profile.objects.filter(user=user_saar).first()
    user_Tal = User.objects.filter(username='Tal').first()
    profile_Tal = Profile.objects.filter(user=user_Tal).first()

    user_event = [
        (profile_ofek, 1),
        (profile_danny, 1),
        (profile_rotem, 1),
        (profile_saar, 1),
        (profile_Tal, 1),

    ]
    with transaction.atomic():
        for profile, event_id in user_event:
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
