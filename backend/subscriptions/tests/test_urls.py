import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer, UserSerializer


# initialize the APIClient app
client = Client()

class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {'username': 'admin', 'email': 'admin@admin.com', 'password': 'password1'}
        response = self.client.post('/account/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='password1')
        self.subscription = Subscription.objects.create(owner=self.user, purchaseDate='2020-12-01T20:25:46.824624Z', paymentMethod='visa', status='True', priceId='price_1HsOMHD3jjDz4sr5mLv7FXy9')
        self.token = Token.objects.create(user=self.user)

    def test_api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_authenticated(self):
        factory = APIRequestFactory()
        request = factory.get('/accounts/django-superstars/')
        response = force_authenticate(request, user=self.user, token=self.token.key)

    def test_get_subscriptions(self):
        response = client.get(reverse('subscriptions-list'))
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_subscription(self):
        response = client.get(
            reverse('subscription', kwargs={'pk': self.subscription.pk}))
        subscription = Subscription.objects.get(pk=self.subscription.pk)
        serializer = SubscriptionSerializer(subscription)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        response = client.get(reverse('user-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_user(self):
        response = client.get(
            reverse('single-user', kwargs={'pk': self.user.pk}))
        user = User.objects.get(pk=self.user.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        response = client.post(
            reverse('register'),
            data=json.dumps({
                'username': 'admin',
                'password': 'password1',
                'subscriptions': [
                    '1'
                ]
            }),
            content_type='application/json'
        )
        user = self.user
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_payment(self):
    #     self.test_setUp()
    #     factory = APIRequestFactory()
    #     user = User.objects.get(username='admin')
    #     view = AccountDetail.as_view()

    #     # Make an authenticated request to the view...
    #     request = factory.get('/accounts/django-superstars/')
    #     force_authenticate(request, user=user)
    #     response = view(request)

        
        