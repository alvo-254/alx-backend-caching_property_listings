from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache view for 15 minutes
def property_list(request):
    properties = get_all_properties()
    data = list(properties.values("id", "title", "price", "location"))
    return JsonResponse(data, safe=False)
