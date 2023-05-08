from django import forms
from .models import Event, Category, Location


class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False)
    poll_end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    poll_max_suggestions = forms.IntegerField(min_value=0)

    class Meta:
        model = Event
        fields = [
            'name',
            'category',
            'location',
            'max_participants',
            'start_time',
            'end_time',
            'poll_end_time',
            'poll_max_suggestions',
            'is_private',
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'poll_end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
