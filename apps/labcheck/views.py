from django.shortcuts import render
from django.http import JsonResponse
from .management.commands.parsehl7 import parse_message, invalid_hl7,  cleanup_hl7
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
	parsed_json = None
	error = None
	if request.method == "POST":
		hl7_input = request.POST.get("hl7-input", "")
		try:
			if invalid_hl7(cleanup_hl7(hl7_input)):
				return render(request, 'labcheck/index.html', {
					"hl7_input": hl7_input,
					"error": "Invalid HL7 message."
				})

			parsed_json = parse_message(cleanup_hl7(hl7_input))[0]
		except Exception as e:
			error = str(e)
	return render(request, 'labcheck/index.html', {
		"hl7_input": request.POST.get("hl7-input", ""),
		"parsed_json": json.dumps(parsed_json, indent=4) if parsed_json else None,
		"error": error
	})

@csrf_exempt
def api_index(request):
	if request.method == "POST":
		hl7_file = request.FILES.get("hl7_file")
		if not hl7_file:
			return JsonResponse({"error": "No HL7 file uploaded."}, status=400)
		try:
			hl7_content = hl7_file.read().decode("utf-8")
			if invalid_hl7(cleanup_hl7(hl7_content)):
				error ={"hl7_input": hl7_content,"error": "Invalid HL7 message."}
				return JsonResponse(error, status=200, json_dumps_params={'indent': 2})
				
			parsed_json = parse_message(cleanup_hl7(hl7_content))[0]
			return JsonResponse(parsed_json, safe=False, json_dumps_params={'indent': 2})
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=500, json_dumps_params={'indent': 2})
	else:
		return JsonResponse({"error": "Only POST method allowed."}, status=405, json_dumps_params={'indent': 2})