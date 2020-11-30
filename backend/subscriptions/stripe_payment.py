import stripe
import environ

env = environ.Env()
env.read_env() # reading .env file

price_id = env("STRIPE_PRICE_ID")
stripe.api_key = env("STRIPE_SECRET_KEY")

class StripeClass():

    def createPaymentMethod():
        paymentMethod = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 11,
                "exp_year": 2021,
                "cvc": "314",
            },
        )
        return paymentMethod

    def createCustomer():
        createPaymentMethod = StripeClass.createPaymentMethod()
        paymentMethodId = createPaymentMethod['id']
        customer = stripe.Customer.create(
            payment_method=paymentMethodId,
            invoice_settings={
                "default_payment_method": paymentMethodId
            },
            email="bransfieldjack@gmail.com",
            description="myWallSt Test customer"
        )
        return customer

    def updatePaymentMethod():
        pm_ID='pm_1HtDdmD3jjDz4sr5nZhhtKyB'
        paymentUpdate = stripe.PaymentMethod.modify(
            pm_ID,
            metadata={"order_id": "6735"},
        )
        return paymentUpdate

    def createSubscription():
        subscription = stripe.Subscription.create(
            customer="cus_IUCLuOxpAK97Kk",
            items=[
                {"price": price_id},
            ],
        )
        return subscription