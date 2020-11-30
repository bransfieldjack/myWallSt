from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from subscriptions.stripe_payment import StripeClass


@api_view(['GET'])
def api_root(request, format=None):

    # customer = StripeClass.createCustomer()
    subscription = StripeClass.createSubscription()
    # paymentUpdate = StripeClass.updatePaymentMethod()
    print(subscription)

    return Response({
        'users': reverse('user-list', request=request, format=format),
        'subscriptions': reverse('subscriptions-list', request=request, format=format),
        'register': reverse('register', request=request, format=format),
    })

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SubscriptionsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):   # associating the user that created the subscription (perform create allows modification of how instance is saved - handy)

        print("printing request:")
        print(self.request.user)
        print(self.request.data)

        serializer.save(owner=self.request.user)

class SubscriptionsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer