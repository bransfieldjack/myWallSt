from rest_framework import serializers
from subscriptions.models import Subscription
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(many=True, queryset=Subscription.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'subscriptions']

class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Subscription
        fields = ['id', 'owner', 'purchaseDate', 'paymentMethod', 'status', 'priceId']
    