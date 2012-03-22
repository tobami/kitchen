from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

import kitchen.settings as settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'kitchen.dashboard.views.main'),
    # Examples:
    # url(r'^$', 'kitchen.views.home', name='home'),
    # url(r'^kitchen/', include('kitchen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
