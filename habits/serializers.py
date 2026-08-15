from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'duration',
            'is_public',
        )
        read_only_fields = ('user',)

    def validate(self, attrs):
        instance = self.instance

        reward = attrs.get(
            'reward',
            getattr(instance, 'reward', None),
        )
        related_habit = attrs.get(
            'related_habit',
            getattr(instance, 'related_habit', None),
        )
        duration = attrs.get(
            'duration',
            getattr(instance, 'duration', None),
        )
        is_pleasant = attrs.get(
            'is_pleasant',
            getattr(instance, 'is_pleasant', False),
        )
        periodicity = attrs.get(
            'periodicity',
            getattr(instance, 'periodicity', 1),
        )

        if reward and related_habit:
            raise serializers.ValidationError(
                'Нельзя одновременно указывать вознаграждение '
                'и связанную привычку.'
            )

        if duration is not None and duration > 120:
            raise serializers.ValidationError(
                'Время выполнения привычки не может быть больше 120 секунд.'
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                'Связанной может быть только приятная привычка.'
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                'У приятной привычки не может быть вознаграждения '
                'или связанной привычки.'
            )

        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                'Периодичность должна быть от 1 до 7 дней.'
            )

        return attrs
