from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer, UserSerializer
from subscriptions.stripe_payment import StripeClass, webHooks


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Token is required
def payment(request, format=None):
    """
    Process payment, save customer and payment info on success
    """
    stripe_ = StripeClass(request.data)
    stripe_.createPaymentMethod()
    stripe_.createCustomer()
    stripe_.updatePaymentMethod()
    sub = stripe_.createSubscription()
    to_save = {
        "username": request.user,
        "paymentMethod": sub['payment_method']['card']['brand'],
        "status": str(sub['subscription']['plan']['active']),
        "priceId": sub['subscription']['items']['data'][0]['price']['id']
    }
    serializer = SubscriptionSerializer(data=to_save)
    if serializer.is_valid():
        serializer.save(owner=to_save['username'])
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def hooks(request, format=None):
    """
    Handle incoming webhooks from stripe
    """
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

# @api_view(['POST', 'GET'])
# def auth_token(request, format=None):
#     print(request.user)
#     token = Token.objects.create(user=request.user)
#     print(token.key)
#     return Response(token)

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

class SubscriptionsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Single subscription detail
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
