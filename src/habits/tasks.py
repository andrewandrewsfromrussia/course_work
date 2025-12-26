from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .telegram import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(time=current_time).select_related("user")

    for habit in habits:
        user = habit.user
        if not user.telegram_chat_id:
            continue

        if habit.last_notified_at:
            if now - habit.last_notified_at < timedelta(days=habit.periodicity):
                continue

        message = (
            f"Напоминание:\n"
            f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} "
            f"в {habit.place}"
        )

        send_telegram_message(user.telegram_chat_id, message)

        habit.last_notified_at = now
        habit.save(update_fields=["last_notified_at"])

    return "ok"
