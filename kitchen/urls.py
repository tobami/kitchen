from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.http import HttpResponse

from kitchen.dashboard import api
import kitchen.settings as settings


urlpatterns = patterns('',
    (r'^$', 'kitchen.dashboard.views.main'),
    (r'^graph/$', 'kitchen.dashboard.views.graph'),
    (r'^api/nodes', api.get_nodes),
    (r'^api/roles', api.get_roles),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
