from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from myapp.models import  CustomerData

@receiver(post_save, sender= CustomerData)
@receiver(post_delete, sender= CustomerData)
def clear_cache_on_model_change(sender, instance, **kwargs):
    cache.delete(f'customer_data{instance.pk}')
