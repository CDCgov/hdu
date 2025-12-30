from django.urls import path
from .views import index, api_doc, api, api_form_example
app_name = 'fhirec'
urlpatterns = [
    path('', index, name='index'),
    path('api', api, name='api'),
    path('api-form-example/', api_form_example, name='api_form_example'),
    path('api-doc/', api_doc, name='api_doc'),
]
