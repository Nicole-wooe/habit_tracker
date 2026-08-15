from rest_framework import serializers


def validate_reward_and_related_habit(data):
    reward = data.get('reward')
    related_habit = data.get('related_habit')

    if reward and related_habit:
        raise serializers.ValidationError(
            'Нельзя одновременно указывать вознаграждение '
            'и связанную привычку.'
        )


def validate_duration(data):
    duration = data.get('duration')

    if duration is not None and duration > 120:
        raise serializers.ValidationError(
            'Время выполнения привычки не может быть больше 120 секунд.'
        )


def validate_related_habit(data):
    related_habit = data.get('related_habit')

    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            'Связанной может быть только приятная привычка.'
        )


def validate_pleasant_habit(data):
    is_pleasant = data.get('is_pleasant', False)
    reward = data.get('reward')
    related_habit = data.get('related_habit')

    if is_pleasant and (reward or related_habit):
        raise serializers.ValidationError(
            'У приятной привычки не может быть вознаграждения '
            'или связанной привычки.'
        )


def validate_periodicity(data):
    periodicity = data.get('periodicity', 1)

    if periodicity < 1 or periodicity > 7:
        raise serializers.ValidationError(
            'Периодичность должна быть от 1 до 7 дней.'
        )
