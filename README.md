# Kitchen

Kitchen is a Dashboard where you can visualize and browse your servers.
It never has been so easy to find and orginize all your nodes!

## How it works

Data is taken from a Chef repository's node data bag

## Installation

We will need:

* sqlite (or another celery broker)
* python 2.6+
* Django 1.4+
* django-celery
* django-kombu *or* RabbitMQ
* logbook
* littlechef 1.1+
* graphviz
* pydot 1.0.25+ (for graphviz graphs)
* mock (for the unit tests)

They can be installed on Debian or Ubuntu by typing:

`apt-get install sqlite3 graphviz`

`pip install django django-celery django-kombu logbook pydot`

`pip install littlechef`

Then create the celery SQL tables (only necessary if you are using the sqlite
backend):

`python manage.py syncdb`

## Running the development server and job queue

To see the web interface on `localhost:8000`:

`python manage.py runserver`

The repo is configured to work straightaway with the test kitchen, without a need
to configure an external repo and sync it. If you want however to check out the 
sync functionality, you can start the celerybeat job scheduler:

`python manage.py celeryd -B -l info`
