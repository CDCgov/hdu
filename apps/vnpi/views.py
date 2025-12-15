from django.shortcuts import render
from django.http import JsonResponse
from .verify_npi import verify_npi

def index(request):
    return render(request, 'vnpi/index.html')

def api(request, npi_number):
    
    result = verify_npi(npi_number)
    return JsonResponse(result, status=200, json_dumps_params={'indent': 2})


def api_index(request):
    return render(request, 'vnpi/api_index.html')

def api_doc(request):
    return render(request, 'vnpi/api_doc.html')

