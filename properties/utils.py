from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

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

def get_redis_cache_metrics():
    """
    Retrieves cache performance metrics (hits, misses, hit ratio)
    from the default Redis connection.
    """
    try:
        
        conn = get_redis_connection("default")
        
        info = conn.info()
        
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        
        if total > 0:
            hit_ratio = (hits / total) * 100
        else:
            hit_ratio = 0.0
            
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
        
        logger.info(f"Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}%")
        
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }    