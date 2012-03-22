from django.http import HttpResponse
from django.template.loader import render_to_string

from kitchen.lib import get_nodes


def main(request):
    retval, data = get_nodes()
    if retval:
        return HttpResponse(render_to_string('main.html', {'nodes': data}))
    else:
        return HttpResponse(
            render_to_string('kitchen_error.html', {'error': data}))
