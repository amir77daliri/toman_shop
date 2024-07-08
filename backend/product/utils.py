import os
import uuid
from datetime import datetime


def generate_filename(instance, filename):
    base, ext = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex[:10]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"product_images/{timestamp}_{unique_id}_{base}{ext}"
