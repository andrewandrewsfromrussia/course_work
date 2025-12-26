import pytest
from django.contrib.auth import get_user_model

from habits.serializers import HabitSerializer

User = get_user_model()


@pytest.mark.django_db
def test_habit_duration_must_be_120_or_less():
    User.objects.create_user(
        email="u1@example.com", username="u1", password="pass12345"
    )

    data = {
        "place": "home",
        "time": "08:00",
        "action": "drink water",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "tea",
        "duration": 121,
        "is_public": False,
    }

    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "duration" in serializer.errors


@pytest.mark.django_db
def test_habit_cannot_have_reward_and_related_habit_together():
    user = User.objects.create_user(
        email="u2@example.com", username="u2", password="pass12345"
    )

    pleasant = user.habits.create(
        place="bath",
        time="21:00",
        action="take a bath",
        is_pleasant=True,
        periodicity=1,
        duration=60,
        is_public=False,
    )

    data = {
        "place": "home",
        "time": "20:00",
        "action": "walk",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "cookie",
        "related_habit": pleasant.id,
        "duration": 60,
        "is_public": False,
    }

    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_related_habit_must_be_pleasant():
    user = User.objects.create_user(
        email="u3@example.com", username="u3", password="pass12345"
    )

    not_pleasant = user.habits.create(
        place="street",
        time="10:00",
        action="walk",
        is_pleasant=False,
        periodicity=1,
        duration=60,
        is_public=False,
    )

    data = {
        "place": "home",
        "time": "11:00",
        "action": "read",
        "is_pleasant": False,
        "periodicity": 1,
        "related_habit": not_pleasant.id,
        "duration": 60,
        "is_public": False,
    }

    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_pleasant_habit_cannot_have_reward_or_related():
    User.objects.create_user(
        email="u4@example.com", username="u4", password="pass12345"
    )

    data = {
        "place": "home",
        "time": "19:00",
        "action": "watch movie",
        "is_pleasant": True,
        "periodicity": 1,
        "reward": "popcorn",
        "duration": 60,
        "is_public": False,
    }

    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_periodicity_must_be_between_1_and_7():
    User.objects.create_user(
        email="u5@example.com", username="u5", password="pass12345"
    )

    data = {
        "place": "home",
        "time": "07:00",
        "action": "run",
        "is_pleasant": False,
        "periodicity": 8,
        "duration": 60,
        "is_public": False,
    }

    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "periodicity" in serializer.errors
