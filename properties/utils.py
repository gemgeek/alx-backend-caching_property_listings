from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieves all properties, using low-level caching.
    - Tries to get from cache first.
    - If not in cache, fetches from DB and sets cache for 1 hour.
    """
    cache_key = 'all_properties'
    queryset = cache.get(cache_key)
    
    if queryset is None:
        logger.info("Cache miss: Fetching properties from database.")
        queryset = Property.objects.all()
        cache.set(cache_key, queryset, 3600)
    else:
        logger.info("Cache hit: Retrieving properties from cache.")
    
    return queryset