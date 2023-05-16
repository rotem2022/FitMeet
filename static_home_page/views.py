from django.shortcuts import render
from event.models import Event
from location.models import Location
from category.models import Category


def static_home_page(request):
    return render(request, 'home_page/index.html')


def event_list(request):
    events = Event.manager.all()
    if request.method == "POST":
        if 'Choose_filter' in request.POST:
            filter_type = request.POST.get('Choose_filter')

            if filter_type == 'Category' and 'Choose_Category' in request.POST:
                category = request.POST.get('Choose_Category')
                events = events.filter(category__name=category)
            elif filter_type == 'Location' and 'Choose_Location' in request.POST:
                location = request.POST.get('Choose_Location')
                events = events.filter(location__name=location)

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None

    locations = Location.objects.values_list('name', flat=True)
    categories = Category.objects.values_list('name', flat=True)
    context = {'events': events, 'locations': locations, 'categories': categories, 'user_id': user_id}
    return render(request, 'home_page/all_events.html', context)
