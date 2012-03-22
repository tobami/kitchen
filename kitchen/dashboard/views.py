from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.dashboard.chef import get_nodes_extended, get_roles, filter_nodes
from kitchen.settings import REPO


def main(request):
    nodes = filter_nodes(request, get_nodes_extended())
    roles = get_roles()
    environments = set()
    roles_groups = set()
    for role in roles:
        split = role['name'].split('_')
        if split[0] == REPO['ENV_PREFIX']:
            environments.add('_'.join(split[1:]))
        else:
            roles_groups.add(split[0])
    return HttpResponse(render_to_string('main.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': sorted(roles_groups),
                                         'environments': sorted(environments)}))
