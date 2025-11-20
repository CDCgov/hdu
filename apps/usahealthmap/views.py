from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import HealthMap

def index(request):
    """Basic index view"""
    hms = HealthMap.objects.all()
    context = {'healthmaps': hms}
    return render(request, 'usahealthmap/index.html', context= context)


