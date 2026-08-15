from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


User = get_user_model()


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser_habits',
            password='testpassword123',
        )

        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Выпить стакан воды',
            periodicity=1,
            duration=60,
            is_public=False,
        )

    def test_create_habit(self):
        data = {
            'place': 'Спортзал',
            'time': '12:00:00',
            'action': 'Сделать разминку',
            'periodicity': 1,
            'duration': 120,
            'is_public': False,
            'is_pleasant': False,
        }

        response = self.client.post(
            reverse('habits:habit-create'),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list(self):
        response = self.client.get(
            reverse('habits:habit-list'),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        data = {
            'place': 'Кухня',
            'time': '10:00:00',
            'action': 'Выпить стакан воды',
            'periodicity': 1,
            'duration': 60,
            'is_public': False,
            'is_pleasant': False,
        }

        response = self.client.patch(
            reverse(
                'habits:habit-update',
                kwargs={'pk': self.habit.pk},
            ),
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'Кухня')

    def test_delete_habit(self):
        response = self.client.delete(
            reverse(
                'habits:habit-delete',
                kwargs={'pk': self.habit.pk},
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Habit.objects.filter(pk=self.habit.pk).exists()
        )

    def test_duration_validation(self):
        data = {
            'place': 'Дом',
            'time': '15:00:00',
            'action': 'Читать книгу',
            'periodicity': 1,
            'duration': 121,
            'is_public': False,
            'is_pleasant': False,
        }

        response = self.client.post(
            reverse('habits:habit-create'),
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
