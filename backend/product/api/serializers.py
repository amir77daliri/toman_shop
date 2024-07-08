from rest_framework import serializers
from product.models import Product, ProductImage
from decouple import config

MAX_IMG_SIZE = config('MAX_IMG_SIZE', cast=int, default=2097152)
MAX_IMG_PER_PRODUCT = (config('MAX_ING_PER_PRODUCT', cast=int, default=5))


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    new_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'description', 'images', 'new_images')

    def validate_new_images(self, value):
        if len(value) > MAX_IMG_PER_PRODUCT:
            raise serializers.ValidationError(f"Only up to {MAX_IMG_PER_PRODUCT} image could post per product")

        for img in value:
            if img.size > MAX_IMG_SIZE:
                raise serializers.ValidationError(f"image {img} is over 2MB")
        return value

    def create(self, validated_data):
        new_images = validated_data.pop('new_images', [])
        product = Product.objects.create(**validated_data)

        for img in new_images:
            ProductImage.objects.create(product=product, image=img)
        return product

    def update(self, instance, validated_data):
        pass
