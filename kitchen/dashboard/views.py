from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.dashboard.chef import get_nodes, get_roles


def main(request):
    nodes = get_nodes_extended()
    roles = get_roles()
    roles_groups = []
    environments = []
    for role in roles:
        split = role['name'].split('_')
        if split[0] == 'env':
            environments.append('_'.join(split[1:]))
        elif split[0] not in roles_groups:
            roles_groups.append(split[0])
    return HttpResponse(render_to_string('main.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': roles_groups,
                                         'environments': environments}))

