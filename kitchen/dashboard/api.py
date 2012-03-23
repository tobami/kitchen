# -*- coding: utf-8 -*-
import json

from django.core import serializers
from django.http import HttpResponse

from kitchen.dashboard import chef


def get_roles(request):
    roles = chef.get_roles()
    return HttpResponse(json.dumps(roles), content_type="application/json")


def get_nodes(request):
    extended = request.GET.get('extended')
    if extended:
        nodes = chef.get_nodes_extended()
    else:
        nodes = chef.get_nodes()
    return HttpResponse(json.dumps(nodes), content_type="application/json")
