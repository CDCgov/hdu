from django.shortcuts import render

def index(request):
    """Basic index view"""
    return render(request, 'home/index.html')
