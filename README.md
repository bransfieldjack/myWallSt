![](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/Screen+Shot+2020-12-02+at+1.50.51+pm.png)

[![Build Status](https://travis-ci.org/bransfieldjack/myWallSt.svg?branch=master)](https://travis-ci.org/bransfieldjack/myWallSt)

My Wall St DRF/Stripe API Payment Gateway

Notes:

- In order to test webhooks received in response from the Stripe API I used the Stripe CLI tool for local dev

- the .env environment file should be placed in the ./djangostripe directory

## Setup:

### Docker:

Make sure you edit the settings.py file to use the postgres container built from the docker-compose.yml file:

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

You will see something similar to this:

![docker-composeup](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/dockercomposeup.png)

Browse to 'http://0.0.0.0:8000/':

![apiRoot](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/apiRoot.png)

<hr>

### Local:

You can run the app locally using the usual Django command:

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

### Testing:
Make sure you are using local sqlite db conf and not docker postgres conf*
````
python manage.py test
````

## Usage:

### Auth:

Before you can use the API, you will need to add yourself as a user, and generate a token for communication with the payment’s endpoint:

- **From the browsable API**:

- ![userCreate](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/userCreate.png)

- **From postman**:

- ![fromPostman](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/fromPostman.png)

### API:

Endpoints:

- `/` API Root, displays available endpoints. (GET, OPTIONS) 
- `/users` Returns a list of all registered users. (GET, HEAD, OPTIONS)
- `/subscriptions` Returns a list of all valid subscriptions. (GET, HEAD, OPTIONS) 
- `/account/register` Register a new user. (POST, OPTIONS) 
- `/api-token-auth/` Request a token (POST, OPTIONS) 
- `/payment` Submit payment (POST, OPTIONS) 

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
-  Networking:
-  VPC
-  Public and private subnets
-  Routing tables
-  Internet Gateway
-  Key Pairs
-  Security Groups
-  Load Balancers, Listeners, and Target Groups
-  IAM Roles and Policies
-  ECS:
-  Task Definition (with multiple containers)
-  Cluster
-  Service
-  Launch Config and Auto Scaling Group
````

ECR (Elastic container registry) is a repo for storing container images, similar to dockerhub. You have to build, tag and push the API image to it before we can deploy it on ECS.

ECR login command:

````

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <awsAccountID>.dkr.ecr.eu-west-1.amazonaws.com

````

Build app image:

````

docker build -t django-app .

````

Tag image:

````

docker tag django-app:latest <awsAccountID>.dkr.ecr.eu-west-1.amazonaws.com/django-app:latest

````

Push the image to the newly created ECR repo:

````

docker push <awsAccountID>.dkr.ecr.eu-west-1.amazonaws.com/django-app:latest

````

^ Now you have created an image of the DRF API, created an ECR repo in AWS and pushed the image to it for storage/reuse and deployment.

![imagePushed](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/imagePushed.png)

Install terraform with pip/conda.

Run `terraform init` inside the terraform dir to create a new Terraform working directory and download the AWS provider.

In the `variables.tf` file, on line 69, change the `<AWS_ACCOUNT_ID>` to whatever your own AWS Acc ID is before creating resources.

You will also need to create an IAM group(s) with attached permissions: `IAMFullAccess, AmazonECS_FullAccess and AmazonECSTaskExecutionRolePolicy` for your AWS user. (Dont use root :) )

![terraformInit](https://my-wall-st-test.s3-eu-west-1.amazonaws.com/terraformInit.png)

- `terraform plan` generates the execution plan based on the defined configuration.

- `terraform apply` applies the configuration

The `terraform apply` command is used to apply the changes required to reach the desired state of the configuration, or the pre-determined set of actions generated by a `terraform plan` execution plan.

When finished, simply typing `terraform destroy` will remove all of the created resources from your account, and save you money!

