# Kitchen

Kitchen is a Dashboard where you can visualize and browse your servers.
It never has been so easy to find and organize all your nodes!

## How it works

A Chef repository is kept in sync and the node data bag is created. From that,
nodes, roles and environments will be detected, resulting in a browseable 
web interface to your server infrastructure. 

## Installation

We will need:

* sqlite (or another celery broker)
* python 2.6+
* Django 1.4+
* django-celery
* django-kombu *or* RabbitMQ
* logbook
* littlechef 1.2+
* graphviz
* pydot 1.0.26+ (for graphviz graphs)

For tests:

* django-nose
* mock

The dependencies can be installed on Debian or Ubuntu by typing:

    $ apt-get install sqlite3 graphviz

    $ pip install -r requirements.txt


Then create the celery SQL tables (only necessary if you are using the sqlite
backend):

    $ python manage.py syncdb

## Running the development server

To see the web interface on `localhost:8000`:

    $ python manage.py runserver

## Job queue for repo synching
The repo is configured to work straightaway with the test kitchen, without the need
to configure an external repo and sync it. However, if you want to check out the 
sync functionality, you can start the celerybeat job scheduler by issuing:

    $ python manage.py celeryd -B -l info

# Graphs

The graph view dynamically generates a graph of your repository, acording to the
current node selection. Dependencies between nodes are defined by the attributes
`client_roles` and `needs_roles`.

Using the test repo as an example:

* The `webserver` role defines:

```javascript
    "default_attributes": {
        "apache2": {"client_roles": ["loadbalancer"]}
    }
```

That will generate an arrow from `loadbalancer` nodes to `webserver` nodes,
with `apache2` as label.

* The `worker` role defines:

```javascript
    "default_attributes": {
        "mysql": {"needs_roles": ["dbserver"]}
    }
```

That will generate a dashed arrow from `worker` nodes to `dbserver` nodes,
with `mysql` as label.
