# My Wall St DRF/Stripe API Payment Gateway 
<br>

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