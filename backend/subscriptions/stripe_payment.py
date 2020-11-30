import stripe
import environ
from django.http import HttpResponse

env = environ.Env()
env.read_env() # reading .env file

price_id = env("STRIPE_PRICE_ID")
stripe.api_key = env("STRIPE_SECRET_KEY")
endpoint_secret=env("ENDPOINT_SECRET")

class StripeClass(object):

    def __init__(self, request):
        self._request = request
        self._PaymentMethod = None
        self._Customer = None

    def createPaymentMethod(self):
        """
        Creates the payment method. 
        """
        request = self._request
        paymentMethod = stripe.PaymentMethod.create(
            type=request['type'],
            card=request['card'],
        )
        self._PaymentMethod = paymentMethod
        return self._PaymentMethod

    def createCustomer(self):
        customer = stripe.Customer.create(
            payment_method=self._PaymentMethod['id'],
            invoice_settings={
                "default_payment_method": self._PaymentMethod['id']
            },
            email="bransfieldjack@gmail.com",
            description="myWallSt Test customer"
        )
        self._Customer = customer
        return self._Customer

    def updatePaymentMethod(self):
        pm_ID=self._PaymentMethod['id']
        paymentUpdate = stripe.PaymentMethod.modify(
            pm_ID,
            metadata={"customer": self._request['customer']},
        )
        self._PaymentMethod = paymentUpdate
        return paymentUpdate

    def createSubscription(self):
        subscription = stripe.Subscription.create(
            customer=self._PaymentMethod['customer'],
            items=[
                {"price": price_id},
            ],
        )
        return subscription

# ----------------------------------------------------------
# Functions without class:
# ----------------------------------------------------------

def webHooks(request):
    """
    Receive incoming webhook event and process.
    Send email notification via AWS lambda endpoint etc.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'customer.subscription.created':
        subscription = event.data.object # contains a stripe.PaymentIntent
        print('Customer subscription created')
        print(type(subscription))
        print(subscription)
        return subscription
    elif event.type == 'customer.subscription.updated':
        subscription = event.data.object # contains a stripe.PaymentMethod
        print('Customer subscription updated')
        print(subscription)
        return subscription
    # ... handle other event types
    else:
        return HttpResponse(status=200)
        # print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

