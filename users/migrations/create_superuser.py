from __future__ import unicode_literals
from django.db import migrations, transaction
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    with transaction.atomic():
        superuser = User(
            is_superuser=True, is_staff=True, username='admin', email='admin@gmail.com'
        )
        superuser.set_password('adminPassword')
        superuser.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_superuser)]
