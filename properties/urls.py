from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('search/', views.search_results, name='search_results'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('api/locations/', views.location_autocomplete, name='location_autocomplete'),
]
