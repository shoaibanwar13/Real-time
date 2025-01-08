# In your app's signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import CustomerData
import json

@receiver(post_save, sender=CustomerData)
@receiver(post_delete, sender=CustomerData)
def send_updated_data_to_websocket(sender, instance, **kwargs):
    # Send a message to WebSocket clients when data is updated
    channel_layer = get_channel_layer()
    # You can specify the group name or channel name
    channel_layer.group_send(
        'dashboard_group',  # This group name should match the consumer's group
        {
            'type': 'send_updated_data',  # A custom message handler in your consumer
            'message': 'Data has been updated'
        }
    )
