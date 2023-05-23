from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name="create_event"),
    path('info/', views.view_event, name='view_event'),
    path('event_list/', views.event_list, name='event_list'),
    path('generate_teams/', views.view_generate_teams, name='generate'),
]
