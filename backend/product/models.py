from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decouple import config

from .utils import generate_filename


User = get_user_model()

MAX_IMG_SIZE = config('MAX_IMG_SIZE', cast=int, default=2097152)
MAX_IMG_PER_PRODUCT = (config('MAX_ING_PER_PRODUCT', cast=int, default=5))


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='products', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title or not self.description:
            raise ValidationError(f"title and description could not be empty")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_filename)

    class Meta:
        verbose_name = 'productImage'
        verbose_name_plural = 'productImages'

    def __str__(self):
        return f"{self.image.name} for {self.product}"

    def clean(self):
        # check image size:
        if self.image.size > MAX_IMG_SIZE:
            raise ValidationError("The maximum file size that can be uploaded is 2MB")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.product.images.count() == MAX_IMG_PER_PRODUCT:
            raise ValidationError(f"Max image count for product is {MAX_IMG_PER_PRODUCT}")
        super().save(*args, **kwargs)
