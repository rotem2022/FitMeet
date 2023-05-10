from django.contrib import admin
from .models import Event


class Filter(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "location",
        "is_private",
        "max_participants",
        "participants_num",
        "start_time",
        "end_time",
    )
    list_filter = ("category", "location", "is_private", "max_participants", "participants_num", "start_time")


admin.site.register(Event, Filter)
