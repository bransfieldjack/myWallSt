
![](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/Screen+Shot+2020-12-02+at+1.50.51+pm.png)
 
My Wall St DRF/Stripe API Payment Gateway

Notes: 
- In order to test webhooks received in response from the Stripe API I used the Stripe CLI tool for local dev
- .env environment variables file should be placed in ./djangostripe folder
 
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


## Deployment:

### Heroku:

Procfile: 
````
web: gunicorn djangostripe.wsgi
````
Deploy:
````
git push -u heroku master
````
````
heroku run python manage.py migrate --run-syncdb
````
https://my-wall-st-test.herokuapp.com/

![bonus](https://media.giphy.com/media/KfSgzIWDrFe57CHw6z/giphy.gif)

### AWS ECS via Terraform:

![tf](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/Screen+Shot+2020-12-02+at+3.07.35+pm.png)

[Terraform](https://www.terraform.io/) is a platform agnostic IAC tool.
Similar to travis/docker etc. it uses a declarative model instead of imperative scripting - you describe what you want the end result of your stack to look like, and then the tooling takes care of building it. 

End result of stack build on AWS:

````
-   Networking:
    -   VPC
    -   Public and private subnets
    -   Routing tables
    -   Internet Gateway
    -   Key Pairs
-   Security Groups
-   Load Balancers, Listeners, and Target Groups
-   IAM Roles and Policies
-   ECS:
    -   Task Definition (with multiple containers)
    -   Cluster
    -   Service
-   Launch Config and Auto Scaling Group
-   RDS
-   Health Checks and Logs

````
