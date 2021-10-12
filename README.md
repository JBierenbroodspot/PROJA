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

## Twitter

You need to have an approved developer account for twitter and have access to the Twitter API.

## Dotenv

A file called `.env` is to be placed in the project root. This file contains the following constant.

### Database settings

`DB_NAME`: Name of the database as supplied above.

`DB_USER`: Username assigned to database.

`DB_PASS`: Passphrase used for user.

`DB_PORT`: Port for database. (Default: 5432)

`DB_HOST`: Host adres for database. (Default: 127.0.0.1)

### Django settings

`DJANGO_SECRET`: Secret key used for Django. Since it is exposed already here it is: 
django-insecure-5xt#&&57ek%9+u5d5!crr^um3mpmpz(h*%()73qw+dxn6+31$t

### App settings

`DISPLAY_INTERVAL`: Amount of time that passes before a message is no longer displayed, in hours. (Default: 2)

`WEATHER_API_KEY`: To use this either generate an openweathermap API key yourself or email me for mine.

### Twitter settings

`TWITTER_API`: Consumer key for the Twitter API.

`TWITTER_SECRET`: Consumer secret key for the Twitter API.

`TWITTER_BEARER`: Bearer token for the Twitter API.

`TWITTER_ACCESS_TOKEN`: Access token for user account.

`TWITTER_ACCESS_TOKEN_SECRET`: Access token secret for user account.

`TWITTER_USER`: User id.

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
# Twitter settings
TWITTER_API=
TWITTER_SECRET=
TWITTER_BEARER=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_USER=
# Application settings
DISPLAY_INTERVAL=2
WEATHER_API_KEY=
```

## Requirements

To install requirements run the following command: `pip install -r requirements.txt`

## Migrations

Once everything before here is set up, run the following commands:
* `manage.py makemigrations`
* `manage.py migrate`

## Superuser

You can create a superuser using the `manage.py createsuperuser` command.

## Start

After everything is set up correctly you can start the server by using `manage.py runserver`.

# Project

The project has the following urls to visit:

| url | name | template | view | description |
| --- | --- | --- | --- | --- |
| /station/ | choose_station | select_station_form.html | ChooseStationView | This page is used to select a station from the Station model to visit. This page does not have to be  used and exists purely for ease of development. |
| /station/[int:station_id] | message | message_form.html | MessageView | This page contains a form where users can enter a message containing 140 characters. The station_id parameter in the url corresponds to an id from the Station model. |
| /moderate/ | moderate | moderation_form.html | ModeratorView | This page displays a single message which can be either accepted or denied using a form. The status in the Message model will be set accordingly. The next message will be displayed until there are no more messages. |
| /moderate/denied-messages/ | denied | denied_messages_list.html | DeniedView | This displays a list of all denied messages. |
| /display/[int:station_id] | display | display_list.html | DisplayView | This displays 10 most recently approved messages at a station defined in the url parameter station_id. If there are no recent messages the current weather will be displayed. |
| /display/[int:station_id]/tweets | tweets | display_list.html | TweetView | This displays the 10 most recently posted tweets from all stations. If there are no tweets the current weather will be displayed. |
| /admin/ |  |  |  | Administrators can use this to add users and to modify and create database entries. |
| /login/ |  | login.html |  | Moderators and administrators can use this page to login to be able to access moderation pages. |