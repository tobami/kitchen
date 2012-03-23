from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.dashboard.chef import get_nodes_extended, get_roles, filter_nodes
from kitchen.dashboard import graphs
from kitchen.settings import REPO, SHOW_VIRT_VIEW


def get_data(request):
    filter_env = request.GET.get('env', '')
    filter_roles = request.GET.get('roles','')
    filter_virt = request.GET.get('virt','')
    nodes = get_nodes_extended()
    roles = get_roles()
    environments = [] # an 'implicit' set, as environments must be uniquely named
    roles_groups = set()
    for role in roles:
        split = role['name'].split('_')
        if split[0] == REPO['ENV_PREFIX']:
            name = '_'.join(split[1:])
            environments.append({'name': name, 
                                 'count': len([node for node in nodes if node['chef_environment'] == name])})
        else:
            roles_groups.add(split[0])
    virt_roles = ['host', 'guest']
    # Filter nodes
    if filter_env or filter_roles or filter_virt:
        nodes = filter_nodes(
            filter_env, filter_roles, filter_virt, get_nodes_extended())
    return nodes, roles, roles_groups, environments, virt_roles, filter_env,\
        filter_roles, filter_virt


def main(request):
    nodes, roles, roles_groups, environments, virt_roles, filter_env, \
        filter_roles, filter_virt = get_data(request)
    return HttpResponse(render_to_string('main.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': sorted(roles_groups),
                                         'environments': sorted(environments),
                                         'virt_roles': virt_roles,
                                         'filter_env': filter_env,
                                         'filter_roles': filter_roles,
                                         'filter_virt': filter_virt,
                                         'show_virt': SHOW_VIRT_VIEW}))


def graph(request):
    nodes, roles, roles_groups, environments, virt_roles, filter_env, \
        filter_roles, filter_virt = get_data(request)
    msg = ""
    if not request.GET.get('env'):
        nodes = []
        msg = "Please select an environment"
    graphs.generate_node_map(nodes)
    return HttpResponse(render_to_string('graph.html',
                                        {'nodes': nodes,
                                         'roles': roles,
                                         'roles_groups': sorted(roles_groups),
                                         'environments': sorted(environments),
                                         'filter_env': filter_env,
                                         'filter_roles': filter_roles,
                                         'msg': msg,
                                         }))
