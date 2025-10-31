from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15) 
def property_list(request):
    """
    A view that retrieves all properties from the database,
    serializes them into a list of dictionaries, and returns
    them as a JSON response. The response is cached for 15 minutes.
    """
    
    properties = Property.objects.all()
    
    data = list(properties.values()) 
    
    return JsonResponse(data, safe=False)