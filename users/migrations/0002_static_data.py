from datetime import datetime

from django.db import migrations, transaction


def create_initial_users(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')
    profile_data = [
        ('Ofek', 'qaz[;.123', datetime(2020, 5, 17), '050-123456789'),
        ('Danny', 'qaz[;.123', datetime(2020, 5, 17), '050-223456789'),
        ('Rimon', 'qaz[;.123', datetime(2020, 5, 17), '050-323456789'),
        ('Rotem', 'qaz[;.123', datetime(2020, 5, 17), '050-423456789'),
        ('Saar', 'qaz[;.123', datetime(2020, 5, 17), '050-523456789'),
        ('Tal', 'qaz[;.123', datetime(2020, 5, 17), '050-623456789'),
    ]
    with transaction.atomic():
        for username, password, dob, phone_number in profile_data:
            user = User(username=username, password=password)
            user.save()
            profile = Profile(user=user, date_of_birth=dob, phone_number=phone_number)
            profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', 'create_superuser')
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]
