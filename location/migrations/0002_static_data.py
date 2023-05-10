from django.db import migrations, transaction


def create_initial_locations(apps, schema_editor):
    Location = apps.get_model('location', 'Location')
    location_test_data = [
        ('Bloomfield', 'Tel-Aviv-Yaffo', 'Hatkuma', 10, False, 'A soccer field in tel-aviv'),
        ('Country Club TA A', 'Tel-Aviv-Yaffo', 'Rabbeinu Yerucham', 2, False, 'At the western area'),
        ('Country Club TA B', 'Tel-Aviv-Yaffo', 'Rabbeinu Yerucham', 2, True, 'At the western area'),
        ('Sportsplex Arena', 'Haifa', 'Ben Guriun', 5, False, 'Near the local high-school'),
        ('The Ultimate Sports Hub', 'Haifa', "Ha'Atzma'ut", 33, True, 'For all inside activities'),
        ('Holmes Place Family A', 'Ashdod', 'Barak Ben Avinoam', 10, True, 'At the northern area'),
        ('Holmes Place Family B', 'Ashdod', 'Barak Ben Avinoam', 10, True, 'At the southern area')
    ]
    with transaction.atomic():
        for name, city, street, street_number, indoor, description in location_test_data:
            location = Location(name=name, city=city, street=street, street_number=street_number,
                                indoor=indoor, description=description)
            location.save()


class Migration(migrations.Migration):
    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_locations),
    ]
