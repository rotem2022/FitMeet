from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import pytest
from typing import List
from .. import models

EVENT_NAME = "football with friends"
MAX_PART = 20
IS_PRIVATE = False
DATETIME = timezone.now() + timedelta(days=2)
POLL_END_TIME = timezone.now()
POLL_MAX_SUGGESTIONS = 3


@pytest.fixture
def category1():
    category = models.Category(name="test1")
    category.save()
    return category


@pytest.fixture
def location1():
    location = models.Location(
        name="test1", city="test1", street="test1", street_number=1, indoor=False, description="test1"
    )
    location.save()
    return location


@pytest.fixture
def category_location1(category1, location1):
    cat_loc = models.CategoryLocation(category=category1, location=location1)
    cat_loc.save()
    return cat_loc


@pytest.fixture
def user1():
    user = User.objects.create_user(username='test', password='test', email='myemail@example.com')
    profile = models.Profile(
        user=user, date_of_birth=timezone.now(), phone_number="test", image_url="http://127.0.0.1:8000/"
    )
    profile.save()
    return profile


@pytest.fixture
def user2():
    user = User.objects.create_user(username='test1', password='test1', email='myemail1@example.com')
    profile = models.Profile(
        user=user, date_of_birth=timezone.now(), phone_number="test1", image_url="http://127.0.0.1:8001/"
    )
    profile.save()
    return profile


@pytest.fixture
def poll1():
    poll = models.Poll(max_suggestions=POLL_MAX_SUGGESTIONS, end_time=POLL_END_TIME)
    poll.save()
    return poll


@pytest.fixture
def event1(category_location1, poll1):
    new_event = models.Event(
        category=category_location1.category,
        location=category_location1.location,
        poll=poll1,
        name=EVENT_NAME,
        max_participants=MAX_PART,
        start_time=DATETIME,
        end_time=DATETIME + timedelta(hours=3),
        is_private=IS_PRIVATE,
    )
    new_event.save()
    return new_event


@pytest.fixture
def validate_event1(category_location1, user1):
    event_id = models.Event.manager.create_event(
        category_id=category_location1.category.id,
        location_id=category_location1.location.id,
        name=EVENT_NAME,
        max_participants=MAX_PART,
        start_time=DATETIME,
        end_time=DATETIME + timedelta(hours=3),
        is_private=IS_PRIVATE,
        poll_end_time=POLL_END_TIME,
        poll_suggestions=POLL_MAX_SUGGESTIONS,
        user_id=user1.id,
    )
    event = models.Event.manager.get(id=event_id)
    return event


@pytest.fixture(scope="session")
def categories1(django_db_blocker) -> List[models.Category]:
    with django_db_blocker.unblock():
        query_set = models.Category.objects.all()
        query_set = list(query_set)[:5]
    return query_set


@pytest.fixture(scope="session")
def locations1(django_db_blocker) -> List[models.Location]:
    with django_db_blocker.unblock():
        names = ['Sportech', 'Sami offer stadium', 'Terner stadium', 'Tedi Stadium', 'Bluemfield Stadium']
        cities = ['Tel Aviv', 'Haifa', 'Beer Sheva', 'Jerusalem', 'Yaffo']
        locations_lst = []
        for location_name, city in zip(names, cities):
            new_location = models.Location(
                name=location_name, city=city, street='test', street_number=1, indoor=False, description='test'
            )
            new_location.save()
            locations_lst.append(new_location)
    return locations_lst


@pytest.fixture(scope="session")
def categories_locations1(django_db_blocker, categories1, locations1) -> List[models.CategoryLocation]:
    with django_db_blocker.unblock():
        categories_locations = []
        for category in categories1:
            for location in locations1:
                cat_loc = models.CategoryLocation(category=category, location=location)
                cat_loc.save()
                categories_locations.append(cat_loc)
    return categories_locations


@pytest.fixture(scope="session")
def users1(django_db_blocker) -> List[models.Profile]:
    with django_db_blocker.unblock():
        users = []
        for i in range(25):
            user = User.objects.create_user(username=f'user{i}', password=f'password{i}', email=f'user{i}@example.com')
            profile = models.Profile(
                user=user, date_of_birth=timezone.now(), phone_number=f"user{i}", image_url="http://127.0.0.1:8001/"
            )
            profile.save()
            users.append(profile)

    return users


@pytest.fixture(scope="session")
def time_samples(django_db_blocker):
    with django_db_blocker.unblock():
        current_time = timezone.now()
        lst = [
            current_time + timedelta(days=1),
            current_time + timedelta(days=3),
            current_time + timedelta(weeks=1),
            current_time + timedelta(days=3, weeks=1),
            current_time + timedelta(weeks=3),
        ]
    return lst


@pytest.fixture(scope="session")
def event_data_set(django_db_blocker, categories_locations1, users1, time_samples):
    with django_db_blocker.unblock():
        for index, user in enumerate(users1):
            cat_loc = categories_locations1.pop()
            start_time = time_samples[index % len(time_samples)]
            end_time = start_time + timedelta(hours=3)
            poll_end_time = start_time + timedelta(days=-1)
            models.Event.manager.create_event(
                category_id=cat_loc.category.id,
                location_id=cat_loc.location.id,
                max_participants=2 * index + 2,
                name=f'test event {index}',
                start_time=start_time,
                end_time=end_time,
                is_private=index > 15,
                poll_end_time=poll_end_time,
                poll_suggestions=3,
                user_id=user.id,
            )


@pytest.mark.django_db()
class TestEvent:
    def test_location_category_validation_correct(self, category_location1):
        try:
            models.Event.manager.verify_category_location(
                location_id=category_location1.location.id, category_id=category_location1.category.id
            )
            assert True
        except ValidationError as err:
            pytest.fail(f'An error occurred: {str(err)}')

    def test_location_category_validation_error(self, location1, category1):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.verify_category_location(location_id=location1.id, category_id=category1.id)
        assert err.value.message == models.EventManager.invalid_category_location_message

    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timezone.now() + timedelta(days=1), timezone.now() + timedelta(days=2)),
            (timezone.now() + timedelta(hours=7), timezone.now() + timedelta(hours=10)),
            (timezone.now() + timedelta(minutes=1), timezone.now() + timedelta(minutes=2)),
        ],
    )
    def test_time_validation_correct(self, start_date, end_date):
        try:
            models.Event.manager.verfiy_event_date(start_date, end_date)
            assert True
        except ValidationError as err:
            pytest.fail(f'An error occurred: {str(err)}')

    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timezone.now() + timedelta(days=1), timezone.now()),
            (timezone.now() + timedelta(milliseconds=3), timezone.now()),
            (DATETIME, DATETIME),
        ],
    )
    def test_time_validation_error(self, start_date, end_date):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.verfiy_event_date(start_date, end_date)
        assert err.value.message == models.EventManager.invalid_time_error_message

    def test_poll_end_time_validator(self):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.verify_poll_end_time(
                poll_end_time=timezone.now() + timedelta(days=1), event_start_time=timezone.now()
            )
        assert err.value.message == models.EventManager.invalid_poll_error

    def test_praticipants_validation(self):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.verify_max_participants(max_participants=0, current_participants_num=1)
        assert err.value.message == models.EventManager.invalid_event_size_error

    def test_event_creation_via_manager_and_direct(self, event1, validate_event1):
        assert event1.name == validate_event1.name
        assert event1.location == validate_event1.location
        assert event1.category == validate_event1.category
        assert event1.max_participants == validate_event1.max_participants
        assert event1.max_participants == validate_event1.max_participants
        assert event1.participants_num == validate_event1.participants_num
        assert event1.start_time == validate_event1.start_time
        assert event1.end_time == validate_event1.end_time
        assert event1.is_private == validate_event1.is_private

    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timezone.now(), timezone.now() + timedelta(days=1)),
            (timezone.now(), timezone.now() + timedelta(hours=3)),
            (timezone.now(), timezone.now() + timedelta(minutes=2)),
        ],
    )
    def test_event_update_time_correct(self, validate_event1, start_date, end_date):
        updated_event = models.Event.manager.update(
            event_id=validate_event1.id, start_time=start_date, end_time=end_date
        )
        assert updated_event.start_time.time() == start_date.time()
        assert updated_event.end_time.time() == end_date.time()

    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timezone.now() + timedelta(days=1), timezone.now()),
            (timezone.now() + timedelta(milliseconds=3), timezone.now()),
            (DATETIME, DATETIME),
        ],
    )
    def test_event_update_time_error(self, validate_event1, start_date, end_date):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.update(event_id=validate_event1.id, start_time=start_date, end_time=end_date)
        assert err.value.message == models.EventManager.invalid_time_error_message

    def test_update_category_correct(self, validate_event1):
        cat = models.Category(name="Updated")
        cat.save()
        cat_loc = models.CategoryLocation(category=cat, location=validate_event1.location)
        cat_loc.save()
        updated_event = models.Event.manager.update(event_id=validate_event1.id, category_id=cat.id)
        assert updated_event.category.name == "Updated"

    def test_update_category_error(self, validate_event1):
        cat = models.Category(name="Updated")
        cat.save()
        with pytest.raises(ValidationError) as err:
            models.Event.manager.update(event_id=validate_event1.id, category_id=cat.id)
        assert err.value.message == models.EventManager.invalid_category_location_message

    def test_update_location_correct(self, validate_event1):
        location = models.Location(
            name="update", city="update", street="update", street_number=2, indoor=False, description="update"
        )
        location.save()
        cat_loc = models.CategoryLocation(location=location, category=validate_event1.category)
        cat_loc.save()
        updated_event = models.Event.manager.update(event_id=validate_event1.id, location_id=location.id)
        assert updated_event.location == location

    def test_update_location_error(self, validate_event1):
        with pytest.raises(ValidationError) as err:
            location = models.Location(
                name="update", city="update", street="update", street_number=2, indoor=False, description="update"
            )
            location.save()
            models.Event.manager.update(event_id=validate_event1.id, location_id=location.id)
        assert err.value.message == models.EventManager.invalid_category_location_message

    def test_update_max_participants_correct(self, validate_event1):
        updated_event = models.Event.manager.update(event_id=validate_event1.id, max_participants=MAX_PART + 10)
        assert updated_event.max_participants == MAX_PART + 10

    def test_update_max_participants_erro(self, validate_event1):
        with pytest.raises(ValidationError) as err:
            models.Event.manager.update(event_id=validate_event1.id, max_participants=0)
        assert err.value.message == models.EventManager.invalid_event_size_error

    def test_update_multipule_values(self, validate_event1):
        start_time = timezone.now() + timedelta(weeks=1)
        updated_event = models.Event.manager.update(
            event_id=validate_event1.id,
            name='updated',
            max_participants=MAX_PART + 3,
            start_time=start_time,
            end_time=start_time + timedelta(hours=3),
            is_private=True,
        )
        assert updated_event.name == 'updated'
        assert updated_event.max_participants == MAX_PART + 3
        assert updated_event.start_time == start_time
        assert updated_event.end_time == start_time + timedelta(hours=3)
        assert updated_event.is_private

    def test_update_nothing(self, validate_event1):
        update_event = models.Event.manager.update(event_id=validate_event1.id)
        assert update_event.name == validate_event1.name
        assert update_event.location == validate_event1.location
        assert update_event.category == validate_event1.category
        assert update_event.poll == validate_event1.poll
        assert update_event.start_time == validate_event1.start_time
        assert update_event.end_time == validate_event1.end_time
        assert update_event.is_private == validate_event1.is_private

    def test_join_participant_correct(self, validate_event1, user2):
        current_participants = validate_event1.participants_num
        assert models.Event.manager.join_event(user2.id, validate_event1.id)
        updated_event = models.Event.manager.get(id=validate_event1.id)
        assert updated_event.participants_num == current_participants + 1
        try:
            models.UserEvent.objects.get(userID=user2.id, eventID=validate_event1.id)
            assert True
        except models.UserEvent.DoesNotExist as err:
            pytest.fail(f'An error occurred: {str(err)}')

    def test_join_participant_error_reach_max(self, validate_event1, user2):
        validate_event1.participants_num = MAX_PART
        validate_event1.save()
        assert not models.Event.manager.join_event(user2.id, validate_event1.id)

    def test_join_participant_error_invalid_userid(self, validate_event1):
        participants_num = validate_event1.participants_num
        assert not models.Event.manager.join_event(122, validate_event1.id)
        assert participants_num == validate_event1.participants_num

    def test_object_deleted(self, validate_event1):
        validate_event1.delete()
        assert validate_event1 not in list(models.Event.manager.all())

    @pytest.mark.parametrize(
        "categories,result",
        [(['FootBall'], 5), (['FootBall', 'basketball'], 10), (['Baseball', 'gym', 'football'], 15), (['Chess'], 0)],
    )
    def test_filter_by_category(self, categories, result, event_data_set):
        query_set = models.Event.manager.search(categories=categories)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "location_name, result",
        [(["Tedi stadium"], 5), (["sportech", "Sami offer stadium"], 10), (["Stantiago Bernabeo stadium"], 0)],
    )
    def test_filter_by_location_name(self, location_name, result):
        query_set = models.Event.manager.search(location_names=location_name)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "cities,result",
        [
            (['Tel aviv'], 5),
            (['tel aviv', 'yaffo'], 10),
            (['jerusalem', 'Haifa', 'beer sheva'], 15),
            (['ness ziona'], 0),
        ],
    )
    def test_filter_by_location_city(self, cities, result):
        query_set = models.Event.manager.search(location_cities=cities)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "event_size,result",
        [
            ((8, True), 21),
            ((20, True), 15),
            ((50, False), 25),
            ((1, False), 0),
        ],
    )
    def test_filter_by_event_size(self, event_size, result):
        query_set = models.Event.manager.search(event_size=event_size)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "event_time,result",
        [
            ((timezone.now() + timedelta(days=2), True), 20),
            ((timezone.now() + timedelta(days=9), True), 10),
            ((timezone.now() + timedelta(weeks=2), False), 20),
            ((timezone.now() + timedelta(weeks=4), True), 0),
        ],
    )
    def test_filter_by_event_time(self, event_time, result):
        query_set = models.Event.manager.search(start_time=event_time)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "categories, location_city,result",
        [
            (['FootBall'], ['tel aviv'], 1),
            (['FootBall', 'Basketball'], ['tel aviv'], 2),
            (['FootBall'], ['tel aviv', 'beer sheva'], 2),
            (['chess'], ['bat yam'], 0),
        ],
    )
    def test_filter_by_category_location_city(self, categories, location_city, result):
        query_set = models.Event.manager.search(categories=categories, location_cities=location_city)
        assert len(query_set) == result

    @pytest.mark.parametrize(
        "event_time, event_size,result",
        [
            ((timezone.now() + timedelta(days=2), True), (8, True), 17),
            ((timezone.now() + timedelta(days=9), True), (20, True), 6),
            ((timezone.now() + timedelta(weeks=2), False), (50, False), 20),
        ],
    )
    def test_filter_by_event_time_and_size(self, event_time, event_size, result):
        query_set = models.Event.manager.search(event_size=event_size, start_time=event_time)
        assert len(query_set) == result

    def test_empty_filter(self):
        query_set = models.Event.manager.search()
        assert len(query_set) == 25
