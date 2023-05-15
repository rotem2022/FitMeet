from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import EventForm
from .models import Event


def create_event(request, user_id):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                event_id = Event.manager.create_event(
                    category_id=data['category'].id,
                    location_id=data['location'].id,
                    name=data['name'],
                    max_participants=data['max_participants'],
                    start_time=data['start_time'],
                    end_time=data['end_time'],
                    is_private=data['is_private'],
                    poll_end_time=data['poll_end_time'],
                    poll_suggestions=data['poll_max_suggestions'],
                    user_id=user_id,
                )
                return redirect(f'/{user_id}/event/info/?id={event_id}')
            except ValidationError as err:
                return render(request, 'event/create_event.html', {'form': form, 'error': err.message}, status=409)
        else:
            return render(
                request,
                'event/create_event.html',
                {'form': form, 'error': list(form.errors.values())[0][0]},
                status=409,
            )
    else:
        form = EventForm()
        return render(request, 'event/create_event.html', {'form': form})


def view_event(request, user_id):
    event_id = request.GET["id"]
    event = Event.manager.get(id=event_id)
    return render(request, 'event/event_info.html', {'event': event})
