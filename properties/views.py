from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Property, Location

def property_list(request):
    properties = Property.objects.all()
    
    # Get filter parameters
    property_type = request.GET.get('type')
    bedrooms = request.GET.get('bedrooms')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Apply filters
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    
    if min_price:
        properties = properties.filter(price_per_night__gte=min_price)
    
    if max_price:
        properties = properties.filter(price_per_night__lte=max_price)
    
    # Pagination
    paginator = Paginator(properties, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'property_types': Property.PROPERTY_TYPES,
    }
    return render(request, 'properties/property_list.html', context)


def search_results(request):
    location = request.GET.get('location', '')
    properties = Property.objects.none()
    
    if location:
        properties = Property.objects.filter(
            location__city__icontains=location
        ) | Property.objects.filter(
            location__state__icontains=location
        ) | Property.objects.filter(
            location__country__icontains=location
        )
    
    # Pagination
    paginator = Paginator(properties, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': location,
    }
    return render(request, 'properties/search_results.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property,
    }
    return render(request, 'properties/property_detail.html', context)


def location_autocomplete(request):
    query = request.GET.get('query', '')
    
    if len(query) < 2:
        return JsonResponse({'locations': []})
    
    locations = Location.objects.filter(
        city__icontains=query
    ).values('city', 'state', 'country').distinct()[:10]
    
    suggestions = []
    for loc in locations:
        suggestions.append({
            'city': loc['city'],
            'state': loc['state'],
            'country': loc['country'],
            'display': f"{loc['city']}, {loc['state']}, {loc['country']}"
        })
    
    return JsonResponse({'locations': suggestions})
