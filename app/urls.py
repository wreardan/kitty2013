from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from core.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', login),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login', login),
    url(r'^accounts/logout', logout, {'next_page': '/'}),
    url(r'^accounts/register', register),

    url(r'^user/(\d+)', user_home),

    url(r'^meow/add', add_meow),
    url(r'^meow/remove/(\d+)', remove_meow),
    url(r'^user/subscribe/(\d+)', subscribe_user),
    url(r'^user/unsubscribe/(\d+)', unsubscribe_user)
)
