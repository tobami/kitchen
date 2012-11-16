"""Plugin that adds monitoring links"""


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
