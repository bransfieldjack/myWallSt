from django.db import models


class Subscription(models.Model):

    owner = models.ForeignKey('auth.User', related_name='subscriptions', on_delete=models.CASCADE)
    purchaseDate = models.DateTimeField(auto_now_add=True)
    paymentMethod = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=100, blank=True, default='')
    priceId = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ['purchaseDate']


