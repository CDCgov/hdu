from django.urls import path
from .views import index, api_doc, api, form_example
app_name = 'directcheck'
urlpatterns = [
    path('', index, name='index'),
    path('api/<str:direct_endpoint>', api, name='api'),
    path('form-example/', form_example, name='form_example'),
    path('api-doc/', api_doc, name='api_doc'),
]
