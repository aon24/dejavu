# -*- coding: utf-8 -*- 
"""
AON 2020

"""
# import debug_toolbar

from django.urls import path, re_path, include
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views
from dejavu.settings import STATIC_URL

import api.doGet as doGet
import api.doPost as doPost

from mimetypes import guess_type

# *** *** ***

def showStaticPage(request):
    p = request.META['PATH_INFO']
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponse('', None, 400)

    try:
        with open(f'{STATIC_URL}{p}'.replace('..', ''), 'rb') as f:
            return HttpResponse(f.read(), guess_type(p)[0], 200)
    except:
        return HttpResponse(f'<h3>404<br>Static page "{p}" not found</h3>', None, 200)

# *** *** ***

def dublP(p):
    return HttpResponse('')

urlpatterns = [
    re_path(r'..', dublP),
    # path('', doGet.openDoc),           # /opendoc?form=arm & mode=new

    re_path(r'^pages', doGet.openDoc), # /opendoc?form=a_main & mode=new &
    re_path(r'^opendoc', doGet.openDoc),
    re_path(r'^openpage', doGet.openPage),
    re_path(r'^new', doGet._new),
    re_path(r'^jsv', doGet.jsv),
    re_path(r'^js', doGet.jsv),
    re_path(r'^image', doGet.image),
    re_path(r'^api.getc/', doGet.apiDoGet),
    re_path(r'^api.get/', doGet.apiDoGet),
    re_path(r'^api.post/', doPost.doPost),
    # path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("", views.home, name="home"),
    re_path(r'[\s\S]*', showStaticPage),
]

# *** *** ***

