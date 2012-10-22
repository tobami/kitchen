"""Data API"""
# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from kitchen.dashboard import chef


@require_http_methods(["GET"])
def get_roles(request):
    """Returns all nodes in the repo"""
    roles = chef.get_roles()
    return HttpResponse(json.dumps(roles), content_type="application/json")


@require_http_methods(["GET"])
def get_nodes(request):
    """Returns node files. If 'extended' is given, the extended version is
    returned

    """
    if request.GET.get('extended'):
        nodes = chef.get_nodes_extended()
    else:
        nodes = chef.get_nodes()
    nodes = chef.filter_nodes(nodes, request.GET.get('env'))
    return HttpResponse(json.dumps(nodes), content_type="application/json")
