from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.lib import get_nodes, get_roles


def main(request):
    return HttpResponse(render_to_string('main.html',
                        {'nodes': get_nodes(), 'roles': get_roles()}))
