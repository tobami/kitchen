# Kitchen

Kitchen is a Dashboard where you can visualize and browse your servers.
It never has been so easy to find and organize all your nodes!

## How it works

A Chef repository is kept in sync and the node data bag is created. From that,
nodes, roles and environments will be detected, resulting in a browseable 
web interface to your server infrastructure. 

## Installation

We will need:

* python 2.6+
* Django 1.4+
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

## Running the development server

To see the web interface on `localhost:8000`:

    $ python manage.py runserver

## Repo synching
The repo is configured to work straightaway with the test kitchen, without the need
to configure an external repo and sync it. To resync a repo at any time you can run the repo_sync.py script:

    $ python repo_sync.py

When deploying kitchen to a server a cron job should be added that runs the script
periodically.

# Tags

Kitchen provides Chef tag functionality, taking the tag list defined in [Chef's top-level tags attribute](http://wiki.opscode.com/display/chef/Recipes#Recipes-Tags) and showing them in the dashboard.

It is possible to link a button style for each tag. These are the available button designs:

* `btn-danger`
* `btn-info`
* `btn-inverse`
* `btn-primary`
* `btn-success`
* `btn-warning`

It is possible to link a button style to a specific tag name (or names, with the `*` character) in the settings file:

```python
TAG_CLASSES = {
    "WIP": "btn-warning",
    "dummy": "btn-danger",
    "Node*": "btn-info"
}
```

In that case, `Node*` will define `Node1`, `Node23`, `NodeSpecial3`... If the tag name is not specified in `TAG_CLASSES`, it will have assigned the default button style.

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
