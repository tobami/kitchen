from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

import kitchen.settings as settings


urlpatterns = patterns('',
    (r'^$', 'kitchen.dashboard.views.main'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
