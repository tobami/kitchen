from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.dashboard.chef import get_nodes_extended, get_roles, filter_nodes
from kitchen.dashboard import graphs
from kitchen.settings import REPO, SHOW_VIRT_VIEW


def get_data(request):
    data = {
        'filter_env': request.GET.get('env', ''),
        'filter_roles': request.GET.get('roles', ''),
        'filter_virt': request.GET.get('virt', ''),
    }
    nodes = get_nodes_extended()
    roles = get_roles()
    environments = []  # an 'implicit' set, as envs must be uniquely named
    roles_groups = set()
    for role in roles:
        split = role['name'].split('_')
        if split[0] == REPO['ENV_PREFIX']:
            name = '_'.join(split[1:])
            environments.append({'name': name, 'count': len(
                [node for node in nodes if node['chef_environment'] == name])})
        else:
            roles_groups.add(split[0])
    data['virt_roles'] = ['host', 'guest']
    # Filter nodes
    if data['filter_env'] or data['filter_roles'] or data['filter_virt']:
        nodes = filter_nodes(data['filter_env'], data['filter_roles'],
                             data['filter_virt'], nodes)
    data['nodes'] = nodes
    data['roles'] = roles
    data['roles_groups'] = roles_groups
    data['environments'] = environments
    return data


def main(request):
    data = get_data(request)
    return HttpResponse(
        render_to_string('main.html',
                        {'nodes': data['nodes'],
                        'roles': data['roles'],
                        'roles_groups': sorted(data['roles_groups']),
                        'environments': sorted(data['environments']),
                        'virt_roles': data['virt_roles'],
                        'filter_env': data['filter_env'],
                        'filter_roles': data['filter_roles'],
                        'filter_virt': data['filter_virt'],
                        'show_virt': SHOW_VIRT_VIEW}))


def graph(request):
    data = get_data(request)
    msg = ""
    if not request.GET.get('env'):
        data['nodes'] = []
        msg = "Please select an environment"
    graphs.generate_node_map(data['nodes'])
    return HttpResponse(
        render_to_string('graph.html',
                        {'nodes': data['nodes'],
                        'roles': data['roles'],
                        'roles_groups': sorted(data['roles_groups']),
                        'environments': sorted(data['environments']),
                        'filter_env': data['filter_env'],
                        'filter_roles': data['filter_roles'],
                        'msg': msg,
                        }))
