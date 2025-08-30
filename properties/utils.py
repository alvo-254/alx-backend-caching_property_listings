# properties/utils.py
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    from django.core.cache import cache
    from .models import Property

    properties = cache.get("all_properties")
    if properties is None:
        properties = list(Property.objects.all().values())
        cache.set("all_properties", properties, 3600)  # cache for 1 hour
    return properties


def get_redis_cache_metrics():
    try:
        conn = get_redis_connection("default")
        info = conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0

        logger.info(f"Redis cache metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio}")
        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0,
        }
