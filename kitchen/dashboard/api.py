# -*- coding: utf-8 -*-
import json

from django.core import serializers
from django.http import HttpResponse

from kitchen.lib import load_data


def get_roles(request):
    roles = load_data('data')
    return HttpResponse(json.dumps(roles), content_type="application/json")

def get_nodes(request):
    nodes = load_data('nodes')
    return HttpResponse(json.dumps(nodes), content_type="application/json")
