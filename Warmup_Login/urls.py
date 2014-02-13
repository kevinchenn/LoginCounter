from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Warmup_Login.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

 	url(r'^', include('loginCounter.urls')),
)
