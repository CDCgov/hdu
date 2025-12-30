from django.shortcuts import render
from django.http import JsonResponse
from .forms import FHIRInspectorForm
from .fhirec import fhir_recognizer, check_if_url_is_valid

def index(request):
    return render(request, 'fhirec/index.html')

def api_doc(request):
    return render(request, 'fhirec/api-doc.html')

def api(request):
    url = request.GET.get('url', '')
    include_details = request.GET.get('include_details', 'false').lower()
    if include_details in ['true', 'True']:
        include_details = True
    else:
        include_details = False
    # print(f"Received URL: {url}, Include Details: {include_details}")  # Debug statement

    if not check_if_url_is_valid(url):
        return JsonResponse({'error': f"The provided URL {url} is not valid or reachable."}, status=400)    

    result = fhir_recognizer(url, include_details=include_details)
    
    return JsonResponse(result, status=200, json_dumps_params={'indent': 2})

def api_form_example(request):


    if request.method == 'POST':
        form = FHIRInspectorForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            include_details = form.cleaned_data['include_details']
            result = fhir_recognizer(url, include_details=include_details)
            return JsonResponse(result, status=200, json_dumps_params={'indent': 2})
        else:
            return render(request, 'fhirec/form-example.html', {'form': form})
    else:
        form = FHIRInspectorForm()

    return render(request, 'fhirec/form-example.html', {'form': form})