# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.conf import settings

def static(request, url):
    from utils.decorations import tpls, HttpResponse
    return HttpResponse(tpls('%s.html'%url, dict(), request), content_type='text/html; charset=UTF-8')

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.HOST["STATIC_ROOT"]}),
    (r'^(i/.*)', 'urls.static'),
)


    