from django.db import models
from django.core.exceptions import ValidationError

from .utils import generate_filename


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    MAX_IMAGES_PER_PRODUCT = 5

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_filename)

    class Meta:
        verbose_name = 'productImage'
        verbose_name_plural = 'productImages'

    def __str__(self):
        return f"{self.image.name} for {self.product}"

    def clean(self):
        # check image size:
        max_size = 2 * 1024 * 1024
        if self.image.size > max_size:
            raise ValidationError("The maximum file size that can be uploaded is 2 MB.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.product.images.count() == self.MAX_IMAGES_PER_PRODUCT:
            raise ValidationError("Max image for product is 5")

        super().save(*args, **kwargs)
