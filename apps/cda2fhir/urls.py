from django.conf.urls import include
from django.urls import re_path as url
from django.urls import path, re_path
from django.contrib import admin
author__ = "Alan Viars"
app_name = 'cda2fhir'
from .views import index, api_index
admin.autodiscover()

urlpatterns  = [
    path('', index, name='index'),
    path('api/', api_index, name='api_index'),
]

