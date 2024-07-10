from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImage


@receiver(post_delete, sender=ProductImage)
def delete_images_from_media(sender, instance, **kwargs):
    instance.image.delete(save=False)
