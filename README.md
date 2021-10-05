# Project ns_zuil

A Django project for taking user input, moderating it and displaying it in a nice way.

# Setup

## Database
This project uses a postgresql database. This means you will have to manually create the database first. using these
settings:

| Name | ns_zuil |
| --- | --- |
| Owner | Any owner you'd like |
| Encoding | UTF8 |
| Collation | English_Netherlands.1252 |
| Character type | English_Netherlands.1252 |
| Connection limit | -1 |

## Dotenv

A file called `.env` is to be placed in the project root. This file contains the following constant.

`DB_NAME`: Name of the database as supplied above.

`DB_USER`: Username assigned to database.

`DB_PASS`: Passphrase used for user.

`DB_PORT`: Port for database. (Default: 5432)

`DB_HOST`: Host adres for database. (Default: 127.0.0.1)

`DJANGO_SECRET`: Secret key used for Django. Since it is exposed already here it is: 
django-insecure-5xt#&&57ek%9+u5d5!crr^um3mpmpz(h*%()73qw+dxn6+31$t

`DISPLAY_INTERVAL`: Amount of time that passes before a message is no longer displayed, in hours. (Default: 2)

`WEATHER_API_KEY`: To use this either generate an openweathermap API key yourself or email me for mine.

Template:
```dotenv
# Db settings
DB_NAME=ns_zuil
DB_USER=
DB_PASS=
DB_PORT=5432
DB_HOST=127.0.0.1
# Django settings
DJANGO_SECRET=django-insecure-5xt#&&57ek%9+u5d5!crr^um3mpmpz(h*%()73qw+dxn6+31$t
# Application settings
DISPLAY_INTERVAL=2
WEATHER_API_KEY=
```

## Requirements

To install requirements run the following command: `pip install -r requirements.txt`