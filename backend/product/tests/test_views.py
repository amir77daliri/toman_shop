import tempfile
import shutil

from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from decouple import config

from product.models import Product, ProductImage
from product.utils import generate_photo_file


TEMP_MEDIA = tempfile.mkdtemp()
MAX_IMG_SIZE = config('MAX_IMG_SIZE', cast=int, default=2097152)
MAX_IMG_PER_PRODUCT = (config('MAX_ING_PER_PRODUCT', cast=int, default=5))


class ProductListCreateApiViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Create a test user and obtain JWT token
        self.user = get_user_model().objects.create_user(username='test_user', password='password123')
        self.access_token = self.get_access_token()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA)
        super().tearDownClass()

    def get_access_token(self):
        token = AccessToken.for_user(self.user)
        return str(token)

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_get_products_list(self):
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 20)

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_valid_product_creation(self):
        image_files = []
        for i in range(min(2, MAX_IMG_PER_PRODUCT)):
            img = generate_photo_file()
            image_files.append(img)
        data = {
            'title': "test product creation",
            'price': 120000,
            'description': "Desc for test product creation",
            'new_images': image_files
        }

        # Add authorization header with JWT token
        auth_header = 'Bearer {}'.format(self.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)

        response = self.client.post('/api/v1/products/', data, format='multipart')
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)  # Ensure product ID is returned
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertIn('images', response.data)
        self.assertEqual(len(response.data['images']), len(image_files))

        # Verify database state
        product_id = response.data['id']
        product = Product.objects.get(id=product_id)
        self.assertEqual(product.title, data['title'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.images.count(), len(image_files))

    @override_settings(MEDIA_ROOT=TEMP_MEDIA)
    def test_invalid_product_creation_by_invalid_image_count(self):
        image_files = []
        for i in range(MAX_IMG_PER_PRODUCT+1):
            img = generate_photo_file()
            image_files.append(img)
        data = {
            'title': "test product creation",
            'price': 120000,
            'description': "Desc for test product creation",
            'new_images': image_files
        }

        # Add authorization header with JWT token
        auth_header = 'Bearer {}'.format(self.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth_header)

        response = self.client.post('/api/v1/products/', data, format='multipart')
        self.assertEqual(response.status_code, 400)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(title='test product creation', description='Desc for test product creation')