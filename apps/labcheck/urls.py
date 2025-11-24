from django.urls import path
from .views import index, api_index, api_doc
app_name = 'labcheck'
urlpatterns = [
    path('', index, name='index'),
    path('api/', api_index, name='api_index'),
    path('api-doc/', api_doc, name='api_doc'),
]
