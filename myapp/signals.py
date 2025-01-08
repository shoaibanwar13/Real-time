from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerData

@receiver(post_save, sender=CustomerData)
def notify_changes(instance, created, **kwargs):
    # Only send update notifications when the instance is updated (not created)
    if not created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "updates_group", {
                "type": "database.update",
                "data": {
                    "id": instance.user_id,
                   
                }
            }
        )
