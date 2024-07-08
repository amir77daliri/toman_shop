import tempfile
import shutil

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from product.models import Product, ProductImage
from product.utils import create_image
from decimal import Decimal


TEMP_MEDIA = tempfile.mkdtemp()


class TestProductModel(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            title="product 1 from test",
            price=Decimal('120000'),
            description="product 1 inside test"
        )

    def test_product_creation(self):
        # Invalid products ...
        product_1 = Product(price=Decimal('120000'))  # product without title & desc fields
        product_2 = Product(title='test p2', description="desc of p2")  # product without price field

        with self.assertRaises(ValidationError):
            product_1.save()
        with self.assertRaises(ValidationError):
            product_2.save()

        self.assertEqual(Product.objects.count(), 1)

        # Valid creation
        product_3 = Product.objects.create(title='p3', price=Decimal('20000'), description="desc of p3")

        product_3.save()
        self.assertEqual(Product.objects.count(), 2)


class TestProductImages(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title='Test Product',
            price=Decimal('99.99'),
            description='This is a test product'
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_create_image_within_size_limit(self):
        image = create_image(2 * 1024 * 1024)  # 2 MB
        product_image = ProductImage(product=self.product, image=image)
        product_image.save()
        self.assertEqual(ProductImage.objects.count(), 1)

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_create_image_exceeds_size_limit(self):
        image = create_image(2 * 1024 * 1024 + 1)  # over 2 MB
        product_image = ProductImage(product=self.product, image=image)

        with self.assertRaises(ValidationError):
            product_image.save()

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_max_images_per_product(self):
        for _ in range(5):
            image = create_image(1 * 1024)  # 1 MB
            product_image = ProductImage(product=self.product, image=image)
            product_image.save()

        self.assertEqual(self.product.images.count(), 5)

        image = create_image(1 * 1024)  # 1 MB
        product_image = ProductImage(product=self.product, image=image)
        with self.assertRaises(ValidationError):
            product_image.save()
