# Generated by Django 4.2 on 2023-05-17 09:00

from django.db import migrations
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('manager', event.models.EventManager()),
            ],
        ),
    ]
