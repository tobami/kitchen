"""Dashboard app views"""
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext

from kitchen.dashboard.chef import (get_nodes_extended, get_roles,
    get_environments, filter_nodes, RepoError)
from kitchen.dashboard import graphs
from kitchen.settings import REPO, SHOW_VIRT_VIEW


def _get_data(env, roles, virt):
    """Returns processed repository data, filtering nodes based on given args
    """
    data = {'filter_env': env, 'filter_roles': roles, 'filter_virt': virt}
    nodes = get_nodes_extended()
    data['roles'] = get_roles()
    roles_groups = set()
    for role in data['roles']:
        split = role['name'].split('_')
        if split[0] != REPO['EXCLUDE_ROLE_PREFIX']:
            roles_groups.add(split[0])
    data['roles_groups'] = sorted(roles_groups)
    data['virt_roles'] = ['host', 'guest']
    # Get environments before we filter nodes
    data['environments'] = get_environments(nodes)
    if data['filter_env'] or data['filter_roles'] or data['filter_virt']:
        nodes = filter_nodes(nodes,
            data['filter_env'], data['filter_roles'], data['filter_virt'])
    data['nodes'] = nodes
    return data


def main(request):
    """Default main view showing a list of nodes"""
    data = {}
    try:
        data = _get_data(request.GET.get('env', REPO['DEFAULT_ENV']),
                         request.GET.get('roles', ''),
                         request.GET.get('virt', REPO['DEFAULT_VIRT']))
    except RepoError as e:
        messages.add_message(request, messages.ERROR, str(e))
    else:
        if not len(data['nodes']):
            messages.add_message(request, messages.INFO,
                "There are no nodes that fit the supplied criteria.")
    data['show_virt'] = SHOW_VIRT_VIEW
    data['query_string'] = request.META['QUERY_STRING']
    return render_to_response('main.html',
                              data, context_instance=RequestContext(request))


def graph(request):
    """Graph view where users can visualize graphs of their nodes
    generated using Graphviz open source graph visualization library

    """
    data = {'nodes': []}
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
    data['query_string'] = request.META['QUERY_STRING']
    return render_to_response('graph.html',
                              data, context_instance=RequestContext(request))
