# -*- coding: utf-8 -*- 
"""
AON 2021
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import api.doGet as doGet
import api.doPost as doPost

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

#@login_required
def openDoc(request):
    return doGet.openDoc(request)

#@login_required
def openPage(request):
    return doGet.openPage(request)

#@login_required
def _new(request):
    return doGet._new(request)

#@login_required
def jsv(request):
    return doGet.jsv(request)

#@login_required
def image(request):
    return doGet.image(request)

#@login_required
def apiDoGet(request):
    return doGet.apiDoGet(request)

#@login_required
def doPost(request):
    return doPost.doPost(request)

