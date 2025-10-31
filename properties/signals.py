from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    """
    Invalidates the 'all_properties' cache when a Property
    is saved (created or updated).
    """
    cache.delete('all_properties')
    logger.info("Cache invalidated: 'all_properties' deleted due to save/update.")

@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidates the 'all_properties' cache when a Property
    is deleted.
    """
    cache.delete('all_properties')
    logger.info("Cache invalidated: 'all_properties' deleted due to delete.")