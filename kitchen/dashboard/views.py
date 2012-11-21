"""Dashboard app views"""
import os
import time
import json

from django.contrib.messages import add_message, ERROR, WARNING
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from logbook import Logger

from kitchen.backends.lchef import (get_nodes, get_nodes_extended, get_roles,
                                    get_role_groups, get_environments,
                                    filter_nodes, group_nodes_by_host,
                                    inject_plugin_data, RepoError, plugins as PLUGINS)
from kitchen.dashboard import graphs
from kitchen.settings import (SHOW_VIRT_VIEW, SHOW_HOST_NAMES, SHOW_LINKS,
                              REPO, SYNCDATE_FILE)

log = Logger(__name__)


def _get_data(request, env, roles, virt, group_by_host=False):
    """Returns processed repository data, filtering nodes based on given args
    """
    data = {'filter_env': env, 'filter_roles': roles, 'filter_virt': virt}
    data['roles'] = get_roles()
    roles_groups = get_role_groups(data['roles'])
    data['roles_groups'] = roles_groups
    data['virt_roles'] = ['host', 'guest']
    # Get environments before we filter nodes
    data['nodes'] = get_nodes()
    data['nodes_extended'] = get_nodes_extended(data['nodes'])
    data['environments'] = get_environments(data['nodes_extended'])
    roles_to_filter = '' if group_by_host else data['filter_roles']
    if data['filter_env'] or roles_to_filter or data['filter_virt']:
        data['nodes_extended'] = filter_nodes(data['nodes_extended'],
                                              data['filter_env'],
                                              roles_to_filter,
                                              data['filter_virt'])
    if group_by_host:
        data['nodes_extended'] = group_nodes_by_host(
            data['nodes_extended'], roles=data['filter_roles'])
    inject_plugin_data(data['nodes_extended'])
    if not data['nodes_extended']:
        add_message(request, WARNING,
                    "There are no nodes that fit the supplied criteria.")
    return data


def _show_repo_sync_date(request):
    """Shows the sync date, which will be the modified date of a file"""
    try:
        sync_age = (time.time() - os.stat(SYNCDATE_FILE).st_mtime) / 60
    except OSError:
        add_message(request, ERROR, "There have been errors while "
                                    "syncing the repo")
    else:
        sync_lim = REPO['SYNC_PERIOD'] * 2.5
        if sync_age > sync_lim:
            add_message(request, WARNING, "The {0} repo is getting out of "
                        "sync. Last pull was {1} minutes "
                        "ago.".format(REPO['NAME'], int(sync_age)))


def _set_options(options):
    """Sets default options if none are given"""
    if options is None:
        # Set defaults
        options = ''
        if SHOW_HOST_NAMES:
            options += 'show_hostnames,'
    return options


def main(request):
    """Default main view showing a list of nodes"""
    _show_repo_sync_date(request)
    data = {}
    try:
        data = _get_data(request,
                         request.GET.get('env', REPO['DEFAULT_ENV']),
                         request.GET.get('roles', ''),
                         request.GET.get('virt', REPO['DEFAULT_VIRT']))
    except RepoError as e:
        add_message(request, ERROR, str(e))
    else:
        data['nodes'] = json.dumps(data['nodes'])
    data['show_virt'] = SHOW_VIRT_VIEW
    data['show_links'] = SHOW_LINKS
    data['query_string'] = request.META['QUERY_STRING']
    return render_to_response('main.html',
                              data, context_instance=RequestContext(request))


def virt(request):
    """Displays a view where the nodes are grouped by physical host"""
    _show_repo_sync_date(request)
    data = {}
    try:
        data = _get_data(request,
                         request.GET.get('env', REPO['DEFAULT_ENV']),
                         request.GET.get('roles', ''),
                         None, group_by_host=True)
    except RepoError as e:
        add_message(request, ERROR, str(e))
    else:
        data['nodes'] = json.dumps(data['nodes'])
    data['show_links'] = SHOW_LINKS
    data['query_string'] = request.META['QUERY_STRING']
    return render_to_response('virt.html',
                              data, context_instance=RequestContext(request))


def graph(request):
    """Graph view where users can visualize graphs of their nodes
    generated using Graphviz open source graph visualization library

    """
    _show_repo_sync_date(request)
    data = {}
    options = _set_options(request.GET.get('options'))
    env_filter = request.GET.get('env', REPO['DEFAULT_ENV'])
    try:
        data = _get_data(request, env_filter, request.GET.get('roles', ''),
                         'guest')
    except RepoError as e:
        add_message(request, ERROR, str(e))
    else:
        if env_filter:
            success, msg = graphs.generate_node_map(
                data['nodes_extended'], data.get('roles', []),
                'show_hostnames' in options)
            data['draw_graph'] = success
            if not success:
                add_message(request, ERROR, msg)
        else:
            add_message(request, WARNING, "Please select an environment")

    data['show_hostnames'] = 'show_hostnames' in options
    data['query_string'] = request.META['QUERY_STRING']
    return render_to_response('graph.html',
                              data, context_instance=RequestContext(request))


def plugins(request, name, method, plugin_type='list'):
    """Plugin interface view which either response with the page created by the
    plugin method, or returns a 404 HTTP Error

    """
    try:
        plugin = PLUGINS[name]
    except KeyError:
        raise Http404("Requested plugin '{0}' not found".format(name))
    try:
        func = getattr(plugin, method)
    except AttributeError:
        raise Http404("Plugin '{0}' has no method '{1}'".format(name, method))
    if not getattr(func, '__is_view__', False):
        raise Http404("Plugin method '{0}.{1}' is not defined as a view".format(name, method))
    nodes = get_nodes()
    nodes = get_nodes_extended(nodes)
    if plugin_type in ('v', 'virt'):
        if func.__p_type__ != 'virt':
            raise Http404("Plugin '{0}.{1}' has wrong type".format(name, method))
        nodes = group_nodes_by_host(nodes, roles=None)
    else:
        if func.__p_type__ != 'list':
            raise Http404("Plugin '{0}.{1}' has wrong type".format(name, method))
    inject_plugin_data(nodes)
    try:
        result = func(request, nodes)
    except TypeError:
        raise Http404("Failed running plugin '{0}.{1}'".format(name, method))
    if not isinstance(result, HttpResponseRedirect):
        raise Http404("Plugin '{0}.{1}' returned unexpected result: {2}".format(name, method, result))
    else:
        return result
