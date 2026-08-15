from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminder(chat_id, habit_action, habit_place):
    message = (
        f'Напоминание о привычке!\n\n'
        f'Действие: {habit_action}\n'
        f'Место: {habit_place}'
    )

    return send_telegram_message(chat_id, message)


@shared_task
def check_habits_and_send_reminders():
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    habits = Habit.objects.select_related('user').filter(
        user__telegram_chat_id__isnull=False,
    )

    sent_count = 0

    for habit in habits:
        if habit.time > current_time:
            continue

        if habit.last_notification_date is not None:
            next_notification_date = (
                habit.last_notification_date
                + timedelta(days=habit.periodicity)
            )

            if today < next_notification_date:
                continue

        send_habit_reminder.delay(
            habit.user.telegram_chat_id,
            habit.action,
            habit.place,
        )

        habit.last_notification_date = today
        habit.save(update_fields=['last_notification_date'])

        sent_count += 1

    return sent_count
