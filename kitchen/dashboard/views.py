from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from kitchen.dashboard.chef import (get_nodes_extended, get_roles,
    filter_nodes, RepoError)
from kitchen.dashboard import graphs
from kitchen.settings import REPO, SHOW_VIRT_VIEW


def _get_data(env, roles, virt):
    data = {'filter_env': env, 'filter_roles': roles, 'filter_virt': virt}
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
        nodes = filter_nodes(nodes,
                data['filter_env'], data['filter_roles'], data['filter_virt'])
    data['nodes'] = nodes
    data['roles'] = roles
    data['roles_groups'] = sorted(roles_groups)
    data['environments'] = sorted(environments)
    return data


def main(request):
    data = {}
    try:
        data = _get_data(request.GET.get('env', REPO['DEFAULT_ENV']),
                         request.GET.get('roles', ''),
                         request.GET.get('virt', REPO['DEFAULT_VIRT']))
    except RepoError as e:
        messages.add_message(request, messages.ERROR, str(e))
    else:
        if not len(data['nodes']):
            messages.add_message(request, messages.ERROR,
                "There are no nodes that fit the supplied criteria.")
    data['show_virt'] = SHOW_VIRT_VIEW
    return render_to_response('main.html',
                              data, context_instance=RequestContext(request))


def graph(request):
    data = {}
    env_filter = request.GET.get('env', REPO['DEFAULT_ENV'])
    try:
        data = _get_data(env_filter, request.GET.get('roles', ''), 'guest')
    except RepoError as e:
        messages.add_message(request, messages.ERROR, str(e))

    if not env_filter:
        data['nodes'] = []
        messages.add_message(request,
                             messages.INFO, "Please select an environment")
    graphs.generate_node_map(data['nodes'])
    return render_to_response('graph.html',
                              data, context_instance=RequestContext(request))
