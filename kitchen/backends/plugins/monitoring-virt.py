"""Plugin that adds monitoring links"""

from django.shortcuts import redirect
from kitchen.backends.plugins import is_view


def build_link(data, link):
    data.setdefault('kitchen', {})
    data['kitchen'].setdefault('data', {})
    data['kitchen']['data'].setdefault('links', [])
    data['kitchen']['data']['links'].append(link)


def inject(node):
    """Adds hierarchical monitoring links of the form <domain>/<host>/<guest>
    """
    link = {
        'url': "https://www.google.de/#hl=en&q={0}_{0}".format(node['fqdn']),
        'img': 'http://munin-monitoring.org/static/munin.png',
        'title': 'monitoring',
    }
    build_link(node, link)
    for guest in node.get('virtualization', {}).get('guests', []):
        link = {
            'url': "https://www.google.de/#hl=en&q={0}_{1}".format(
                node['fqdn'], guest['fqdn']),
            'img': 'http://munin-monitoring.org/static/munin.png',
            'title': 'monitoring',
        }
        build_link(guest, link)


@is_view('virt')
def links(request, hosts):
    try:
        fqdn = request.GET['fqdn']
    except KeyError:
        return None
    current_node = None
    for host in hosts:
        if fqdn == host['fqdn']:
            current_node = host
            break
        for node in host.get('virtualization', {}).get('guests', []):
            if fqdn == node['fqdn']:
                current_node = node
                break
        if current_node:
            break
    if current_node:
        try:
            links = current_node['kitchen']['data']['links']
        except KeyError:
            return None
        for link in links:
            if link.get('title') == 'monitoring':
                return redirect(link['url'])
        else:
            return None
