"""Plugin that adds monitoring links"""

from django.shortcuts import redirect
from kitchen.backends.plugins import is_view

def inject(node):
    link = {
        'url': "http://monitoring.mydomain.com/{0}".format(node['fqdn']),
        'img': 'http://munin-monitoring.org/static/munin.png',
        'title': 'monitoring',
    }
    node.setdefault('kitchen', {})
    node['kitchen'].setdefault('data', {})
    node['kitchen']['data'].setdefault('links', [])
    node['kitchen']['data']['links'].append(link)


@is_view
def links(request, nodes):
    try:
        fqdn = request.GET['fqdn']
    except KeyError:
        return None
    for node in nodes:
        if fqdn == node['fqdn']:
            links = node['kitchen']['data']['links']
            for link in links:
                if link.get('title') == 'monitoring':
                    return redirect(link['url'])
