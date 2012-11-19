# Kitchen

![Example list view](http://ahye.edelight.net/s/B4SGViOc.png)

Kitchen is a Dashboard where you can visualize and browse your servers.
It has a node _list_ view, a hardware centric _virt_ view where nodes are grouped by
host, and a _graph_ view that dynamically generates graphs of your infrastructure.
It never has been easier to find and organize all your nodes!

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

Distro package dependencies can be installed on Debian or Ubuntu by typing:

    $ apt-get install sqlite3 graphviz

while all Python dependencies can be install by using `requirements.txt` and `test_requirements.txt`:

    $ pip install -r requirements.txt && pip install -r test_requirements.txt

## Running the development server

To give the web interface a try use the development server on `localhost:8000`:

    $ python manage.py runserver

## Repo synching

To resync a repo at any time you can run the `repo_sync.py` script:

    $ python repo_sync.py

When deploying kitchen to a server a cron job should be added that runs the script
periodically.

You should be able to play around with the test kitchen straightaway. You can
configure you own repo in `settings.py` by properly configuring the `REPO_BASE_PATH`
and `REPO` variables.

## Tags

The tag column will show any string in the list defined by top-level [Chef "tags" attribute](http://wiki.opscode.com/display/chef/Recipes#Recipes-Tags).

It is possible to assign different colors to the tag buttons by mapping tag names to css styles:
```python
TAG_CLASSES = {
    "WIP": "btn-warning",
    "dummy": "btn-danger",
    "Node*": "btn-info"
}
```
Available [bootstrap CSS styles](http://twitter.github.com/bootstrap/base-css.html#buttons): `btn-danger`, `btn-info`, `btn-inverse`, `btn-primary`, `btn-success` and `btn-warning`

## Links

The dashboard will show any links to external systems (for example monitoring or
admin interfaces) it finds on `kitchen/data/links/`. The format is:

```javascript
{
    "url": "http://testnode1:22002",
    "img": "http://your.image.domain/haproxy-logo.png",
    "title": "haproxy"
}
```
If the "img" field is not present, a text link will be shown instead of an image.

If you don't want to clutter your node files with link data, you can use link plugins
to generate the links on the fly. Just save the plugin in the `backends/plugins/` dir
and add the plugin name to `ENABLE_PLUGINS`.

The link column can be deactivated with the option `SHOW_LINKS`.

# Views

## Virt

![Example virt view](http://ahye.edelight.net/s/yWF1ixAv.png)

Virt groups nodes by host to present a close-to-the-hardware view to your
nodes. That is done by fetching all nodes with the Chef attribute `virtualization/role`
set to `host`, looking at all the `virtualization/guests` entries, and adding the
corresponding "guest" nodes to the list.

This view is optional and can be deactivated in `settings.py` by setting 
`SHOW_VIRT_VIEW` to `False`.

Note: Filtering by using the left nav bar will show all hosts with all their guests that
have at least a guest containing one of the selected roles. Filtering by using the
search field will only show matching guests.

## Graphs

![Example graph](http://ahye.edelight.net/s/1SvFxpPi.png)

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
