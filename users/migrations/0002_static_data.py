from datetime import datetime

from django.db import migrations, transaction
from django.contrib.auth.hashers import make_password


def create_initial_users(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')
    profile_data = [
        ('Ofek', 'ofekPassword', datetime(2020, 5, 17), '050-123456789'),
        ('Danny', 'dannyPassword', datetime(2020, 5, 17), '050-223456789'),
        ('Rimon', 'rimonPassword', datetime(2020, 5, 17), '050-323456789'),
        ('Rotem', 'rotemPassword', datetime(2020, 5, 17), '050-423456789'),
        ('Saar', 'saarPassword', datetime(2020, 5, 17), '050-523456789'),
        ('Tal', 'talPassword', datetime(2020, 5, 17), '050-623456789'),
    ]
    with transaction.atomic():
        for username, password, dob, phone_number in profile_data:
            encrypted_pw = make_password(password)
            user = User(username=username, password=encrypted_pw)
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
