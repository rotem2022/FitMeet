from django.db import migrations, transaction


def create_initial_locations(apps, schema_editor):
    CategoryLocation = apps.get_model('category_location', 'CategoryLocation')
    Location = apps.get_model('location', 'Location')
    Category = apps.get_model('category', 'Category')
    soccer = Category.objects.filter(name="Soccer").first()
    football = Category.objects.filter(name="Football").first()
    basketball = Category.objects.filter(name='Basketball').first()
    baseball = Category.objects.filter(name='Baseball').first()
    gym = Category.objects.filter(name='Gym').first()
    track_and_field = Category.objects.filter(name='Track and field').first()
    bloomfield = Location.objects.filter(name="Bloomfield").first()
    country_club_ta_a = Location.objects.filter(name='Country Club TA A').first()
    country_club_ta_b = Location.objects.filter(name='Country Club TA B').first()
    sportsplex_arena = Location.objects.filter(name='Sportsplex Arena').first()
    the_ultimate_sports_hub = Location.objects.filter(name='The Ultimate Sports Hub').first()
    holmes_place_family_a = Location.objects.filter(name='Holmes Place Family A').first()
    holmes_place_family_b = Location.objects.filter(name='Holmes Place Family B').first()
    category_location_data = [
        (bloomfield, soccer),
        (country_club_ta_a, soccer),
        (country_club_ta_a, football),
        (country_club_ta_a, baseball),
        (country_club_ta_a, track_and_field),
        (country_club_ta_b, basketball),
        (country_club_ta_b, gym),
        (country_club_ta_b, football),
        (sportsplex_arena, basketball),
        (sportsplex_arena, soccer),
        (sportsplex_arena, track_and_field),
        (the_ultimate_sports_hub, soccer),
        (the_ultimate_sports_hub, football),
        (the_ultimate_sports_hub, basketball),
        (the_ultimate_sports_hub, baseball),
        (the_ultimate_sports_hub, gym),
        (the_ultimate_sports_hub, track_and_field),
        (holmes_place_family_a, gym),
        (holmes_place_family_a, basketball),
        (holmes_place_family_b, football),
        (holmes_place_family_b, track_and_field)
    ]
    with transaction.atomic():
        for location, category in category_location_data:
            category_location = CategoryLocation(category=category, location=location)
            category_location.save()


class Migration(migrations.Migration):
    dependencies = [
        ('category_location', '0001_initial'),
        ('category', '0002_static_data'),
        ('location', '0002_static_data'),
    ]

    operations = [
        migrations.RunPython(create_initial_locations),
    ]
