import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer, UserSerializer


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {'username': 'admin', 'email': 'admin@admin.com', 'password': 'password1'}
        response = self.client.post('/account/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ViewSetTestCase(APITestCase):

    # list_url = reverse('api-auth')

    def test_setUp(self):
        self.user = User.objects.create_user(username='admin', password='password1')
        self.token = Token.objects.create(user=self.user)
        self.test_api_authentication()

    def test_api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    # def test_authenticated(self):
    #     response = self.client.get(list_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

        