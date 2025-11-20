from django.urls import path
from .views import index, api_index
app_name = 'labcheck'
urlpatterns = [
    path('', index, name='index'),
    path('api/', api_index, name='api_index'),
]
