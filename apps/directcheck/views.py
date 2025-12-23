from django.shortcuts import render
from django.http import JsonResponse
from gdc.get_direct_certificate import DCert
from .forms import DirectCheckForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
#sheela.a.bhat.upmcdirect.com


def form_example(request):
    if request.method == 'POST':
        
        form = DirectCheckForm(request.POST)
        if form.is_valid():
            endpoint = form.cleaned_data['endpoint']
            messages.success(request, f'Success! One or more certifictes were found for Direct endpoint "{endpoint}".')
            return HttpResponseRedirect(reverse("directcheck:form_example"))
        else:
            return render(request, 'directcheck/form-example.html', {'form': form})
    context = {'form': DirectCheckForm()}
    return render(request, 'directcheck/form-example.html', context)

def index(request):
    return render(request, 'directcheck/index.html')

def api(request, direct_endpoint):
    # Placeholder for actual direct check logic

    dc = DCert(direct_endpoint)
    dc.validate_certificate(False) 
    return JsonResponse(dc.result, status=200, json_dumps_params={'indent': 2})


def api_doc(request):
    return render(request, 'directcheck/api-doc.html')