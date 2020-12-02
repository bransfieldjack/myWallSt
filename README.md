
![](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/Screen+Shot+2020-12-02+at+1.50.51+pm.png)
 
My Wall St DRF/Stripe API Payment Gateway

 
## Setup:

### Docker:
Make sure you edit the settings.py file to use the postgres container built form the docker-compose.yml file:
````
DATABASES  = {
	'default': { # Default config for docker
	'ENGINE': 'django.db.backends.postgresql',
	'NAME': 'postgres',
	'USER': 'postgres',
	'PASSWORD': 'postgres',
	'HOST': 'db',
	'PORT': 5432,
	},
}
````
Start the app with the following command:
````
docker-compose up
````
You should see something similer to this:

![docker-composeup](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/dockercomposeup.png)

Browser to 'http://0.0.0.0:8000/':

![apiRoot](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/apiRoot.png)

<hr>

### Local:

You can run the app locally using the usual Django command
````
python manage.py runserver
````

Just remember to revert the database settings to use the sqlite db:

````
'default': { 
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
````
<hr>

## Usage:

### Auth:
Before you can use the API, you will need to add yourself as a user, and generate a token for communication with the payments endpoint:

- **From the browsable API**:
	- ![userCreate](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/userCreate.png)

- **From postman**: 
	- ![fromPostman](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/fromPostman.png)

### API:
Before you can submit a payment request for a stripe subscription, you will need to generate an auth token  (postman) using the newly registered account:

![authToken](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/authToken.png)

With the generated token you can submit a payment request to the 'http://0.0.0.0:8000/payment/' endpoint:

![paymentEndpoint](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/paymentEndpoint.png)

The payload structure (body) for the request:

````
{
	"paymentMethod":  "mastercard",
	"type":  "card",
	"card":  {
		"number":  "4242424242424242",
		"exp_month":  11,
		"exp_year":  2021,
		"cvc":  "314"
	},
	"customer":  "bransfieldjack@gmail.com"
}
````