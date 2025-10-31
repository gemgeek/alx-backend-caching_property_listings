from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15) # Keep the view-level cache
def property_list(request):
    """
    A view that retrieves all properties from the database,
    serializes them into a list of dictionaries, and returns
    them as a JSON response. The response is cached for 15 minutes.
    
    This view now uses the low-level cached get_all_properties() function.
    """
    
    properties = get_all_properties()
    
    data = list(properties.values()) 
    
    return JsonResponse({"properties": data})