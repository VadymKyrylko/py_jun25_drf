from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from messenger.models import Tag, Message
from messenger.tasks import send_new_message_notification


@receiver([post_save, post_delete], sender=Tag)
def invalidate_tag_list_cache(sender, instance, **kwargs):
    cache.delete_pattern("*tag-list*")


@receiver([post_save], sender=Message)
def send_message_created_notification(sender, instance, created, **kwargs):
    if created:
        send_new_message_notification.delay_on_commit(instance.id)
