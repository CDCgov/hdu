from django.shortcuts import render

def index(request):
    """Basic index view"""
    return render(request, 'index.html')
