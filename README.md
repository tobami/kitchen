# Kitchen

Kitchen is a Dashboard where you can visualize and browse your servers.
It never has been so easy to find and orginize all your nodes!

## How it works

Data is taken from a Chef repository's node data bag

## Installation

We will need sqlite, python 2.6+, Django 1.3+ and django-celery

`apt-get install sqlite3`
`pip install django django-celery`

Then create the necessary celery tables

`python manage.py syncdb`
