import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


@pytest.mark.django_db
def test_user_sees_only_own_habits_in_list():
    client = APIClient()

    u1 = User.objects.create_user(
        email="a@example.com", password="pass12345"
    )
    u2 = User.objects.create_user(
        email="b@example.com", password="pass12345"
    )

    Habit.objects.create(
        user=u1, place="home", time="08:00", action="A",
        is_pleasant=False, periodicity=1, duration=60, is_public=False
    )
    Habit.objects.create(
        user=u2, place="home", time="09:00", action="B",
        is_pleasant=False, periodicity=1, duration=60, is_public=False
    )

    client.force_authenticate(user=u1)
    resp = client.get("/api/habits/")

    assert resp.status_code == 200
    assert resp.data["count"] == 1
    assert resp.data["results"][0]["action"] == "A"


@pytest.mark.django_db
def test_public_habits_list_shows_only_public():
    client = APIClient()

    user = User.objects.create_user(
        email="p@example.com", password="pass12345"
    )

    Habit.objects.create(
        user=user, place="home", time="08:00", action="public",
        is_pleasant=False, periodicity=1, duration=60, is_public=True
    )
    Habit.objects.create(
        user=user, place="home", time="09:00", action="private",
        is_pleasant=False, periodicity=1, duration=60, is_public=False
    )

    resp = client.get("/api/habits/public/")

    assert resp.status_code == 200
    assert resp.data["count"] == 1
    assert resp.data["results"][0]["action"] == "public"


@pytest.mark.django_db
def test_user_cannot_update_foreign_habit():
    client = APIClient()

    u1 = User.objects.create_user(
        email="o1@example.com", password="pass12345"
    )
    u2 = User.objects.create_user(
        email="o2@example.com", password="pass12345"
    )

    habit = Habit.objects.create(
        user=u1,
        place="home",
        time="08:00",
        action="foreign",
        is_pleasant=False,
        periodicity=1,
        duration=60,
        is_public=False,
    )

    client.force_authenticate(user=u2)
    resp = client.patch(
        f"/api/habits/{habit.id}/",
        {"action": "hacked"},
        format="json",
    )

    assert resp.status_code in (403, 404)


@pytest.mark.django_db
def test_create_habit_sets_user_automatically():
    client = APIClient()
    user = User.objects.create_user(
        email="c@example.com", password="pass12345"
    )
    client.force_authenticate(user=user)

    payload = {
        "place": "home",
        "time": "08:30",
        "action": "create",
        "is_pleasant": False,
        "periodicity": 1,
        "duration": 60,
        "is_public": False,
    }

    resp = client.post("/api/habits/", payload, format="json")
    assert resp.status_code == 201
    assert resp.data["user"] == user.id
