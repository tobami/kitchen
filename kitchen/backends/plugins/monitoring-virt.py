"""Plugin that adds monitoring links"""


def build_link(data, link):
    data.setdefault('kitchen', {})
    data['kitchen'].setdefault('data', {})
    data['kitchen']['data'].setdefault('links', [])
    data['kitchen']['data']['links'].append(link)


def inject(node):
    """Adds hierarchical monitoring links of the form <domain>/<host>/<guest>
    """
    link = {
        'url': "http://monitoring.mydomain.com/{0}/{0}".format(node['fqdn']),
        'img': 'http://munin-monitoring.org/static/munin.png',
        'title': 'monitoring',
    }
    build_link(node, link)
    for guest in node.get('virtualization', {}).get('guests', []):
        link = {
            'url': "http://monitoring.mydomain.com/{0}/{1}".format(
                node['fqdn'], guest['fqdn']),
            'img': 'http://munin-monitoring.org/static/munin.png',
            'title': 'monitoring',
        }
        build_link(guest, link)
