from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from messenger.models import Tag


@receiver([post_save, post_delete], sender=Tag)
def invalidate_tag_list_cache(sender, instance, **kwargs):
    cache.delete_pattern("*tag-list*")
