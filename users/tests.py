from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPassword123!',
            'telegram_chat_id': 123456789,
        }

        response = self.client.post(
            reverse('register'),
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )

        user = User.objects.get(username='newuser')

        self.assertNotEqual(
            user.password,
            'TestPassword123!',
        )

        self.assertTrue(
            user.check_password('TestPassword123!')
        )

    def test_login_user(self):
        User.objects.create_user(
            username='loginuser',
            password='TestPassword123!',
        )

        data = {
            'username': 'loginuser',
            'password': 'TestPassword123!',
        }

        response = self.client.post(
            reverse('login'),
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
