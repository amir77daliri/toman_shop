from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImage


@receiver(post_delete, sender=ProductImage)
def tell_people(sender, instance, **kwargs):
    instance.image.delete(save=False)
