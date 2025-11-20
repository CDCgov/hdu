from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from fhir_converter.renderers import  CcdaRenderer
import json

def index(request):
    
    if request.method == "POST":
        xml_in = request.POST.get("cda-input", "")
        try:
            fhir_bundle_json = CcdaRenderer().render_fhir_string("CCD", xml_in)
        except Exception as e:
            fhir_bundle_json = {"error": str(e), "message": e.__class__.__name__, "cause": str(e.__cause__)}


        return render(request, 'cda2fhir/index.html', {
            "cda_input": xml_in,
            "fhir_output": fhir_bundle_json
        })
    else:
        return render(request, 'cda2fhir/index.html')
@csrf_exempt
def api_index(request):
    if request.method == "POST":
        cda_file = request.FILES.get("cda_file")
        if not cda_file:
            return JsonResponse({"error": "No CDA file uploaded."}, status=400)
        try:
            xml_in = cda_file.read().decode("utf-8")
            fhir_bundle_json = CcdaRenderer().render_fhir_string("CCD", xml_in)
            fhir_bundle_json = json.dumps(json.loads(fhir_bundle_json), indent=2)
            return HttpResponse(fhir_bundle_json, content_type='application/json')
        except Exception as e:
            return JsonResponse({
                "error": str(e),
                "message": e.__class__.__name__,
                "cause": str(e.__cause__)
            }, status=500)
    else:
        return JsonResponse({"error": "Only POST method allowed."}, status=405)