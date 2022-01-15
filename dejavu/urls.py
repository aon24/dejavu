# -*- coding: utf-8 -*- 
"""
AON 2020

"""
# import debug_toolbar

from django.urls import path, re_path, include
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import views as auth_views

import dejavu.views as views
from dejavu.settings import STATIC_URL

from mimetypes import guess_type
import os

# *** *** ***

def showStaticPage(request):
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponse('', None, 400)

    try:
        p = os.path.join(STATIC_URL, request.META['PATH_INFO'][1:])
        with open(p.replace('..', ''), 'rb') as f:
            return HttpResponse(f.read(), guess_type(p)[0], 200)
    except:
        return HttpResponse(f'<h3>404<br>Static page "{p}" not found</h3>', None, 200)

# *** *** ***

def dublP(p):
    return HttpResponse('')

urlpatterns = [
    re_path(r'\.\.', dublP),
    # path('', doGet.openDoc),           # /opendoc?form=arm & mode=new

    path('', views.openDoc), # form=irm & mode=new
    re_path(r'^pages', views.openDoc), # /opendoc?form=a_main & mode=new &
    re_path(r'^opendoc', views.openDoc),
    re_path(r'^openpage', views.openPage),
    re_path(r'^new', views._new),
    re_path(r'^jsv', views.jsv),
    re_path(r'^js', views.jsv),
    re_path(r'^image', views.image),
    re_path(r'^api.getc/', views.apiDoGet),
    re_path(r'^api.get/', views.apiDoGet),
    re_path(r'^api.post/', views.doPost),
    # path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    ]

urlpatterns += [
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    # path("", views.home, name="home"),
    re_path(r'[\s\S]*', showStaticPage),
]

# *** *** ***

