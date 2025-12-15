from django.urls import path
from .views import index, api_doc, api
app_name = 'vnpi'
urlpatterns = [
    path('', index, name='index'),
    path('api/<str:npi_number>', api, name='api'),
    path('api-doc/', api_doc, name='api_doc'),
]
