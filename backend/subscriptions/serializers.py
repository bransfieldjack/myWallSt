from django.contrib.auth.models import User
from rest_framework import serializers

from subscriptions.models import Subscription


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(many=True, queryset=Subscription.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'subscriptions']
        extra_kwargs = {'password': {'write_only': True}}   # Hides password in API

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)   # Inherit parent class methods and hash password. 
        user.set_password(validated_data['password'])
        user.save()
        return user

class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Subscription
        fields = ['id', 'owner', 'purchaseDate', 'paymentMethod', 'status', 'priceId']
    
    