from django.urls import path
from .views import index
from django.contrib import admin
admin.autodiscover()
author__ = "Alan Viars"
app_name = 'usahealthmap'

urlpatterns = [
    path('', index, name='index'),
]
