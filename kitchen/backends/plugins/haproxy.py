"""Plugin that adds haproxy links"""


def build_link(data):
    if "haproxy::app_lb" not in data['recipes']:
        return
    domain = data['fqdn']
    link = {
        'url': "http://{0}:22002".format(domain),
        'title': 'haproxy',
    }
    data.setdefault('kitchen', {})
    data['kitchen'].setdefault('data', {})
    data['kitchen']['data'].setdefault('links', [])
    data['kitchen']['data']['links'].append(link)


def inject(node):
    """Adds haproxy links to hosts and guests"""
    build_link(node)
    for guest in node.get('virtualization', {}).get('guests', []):
        build_link(guest)
