from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from subscriptions.stripe_payment import StripeClass, webHooks


@api_view(['POST'])
def payment(request, format=None):
    _stripe = StripeClass(request.data)
    _stripe.createPaymentMethod()
    _stripe.createCustomer()
    _stripe.updatePaymentMethod()

    sub = _stripe.createSubscription()
    # print(sub)

    return Response(sub)

@api_view(['POST'])
def hooks(request, format=None):
    res = webHooks(request)
    return res

@api_view(['GET'])
def api_root(request, format=None):
    """
    Root API view
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'subscriptions': reverse('subscriptions-list', request=request, format=format),
        'register': reverse('register', request=request, format=format),
    })

class UserCreate(generics.CreateAPIView):
    """
    Create/register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserList(generics.ListAPIView):
    """
    Return all registered users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    """
    Get single user, delete
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SubscriptionsList(generics.ListAPIView):
    """
    Returns a list of subscriptions and their subscribers (user).
    Create new subscription, extended with 'perform_create' to append verified user to the subscription.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # def perform_create(self, serializer):   # associating the user that created the subscription (perform create allows modification of how instance is saved - handy)
    #     return Response(status=200)

class SubscriptionsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer