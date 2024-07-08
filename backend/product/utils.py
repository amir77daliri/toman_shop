import io
import os
import uuid

from datetime import datetime

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_filename(instance, filename):
    base, ext = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex[:10]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"product_images/{timestamp}_{unique_id}_{base}{ext}"


def create_image(size):
    file = io.BytesIO()
    file.write(b'\x00' * size)
    file.seek(0)
    image = SimpleUploadedFile('test_image.jpg', file.read(), content_type='image/jpeg')
    return image


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(10, 10), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file
