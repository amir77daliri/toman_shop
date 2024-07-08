from rest_framework import serializers
from product.models import Product, ProductImage


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
        if len(value) > 5:
            raise serializers.ValidationError("Only up to 5 image could post per product")

        max_size = 2 * 1024 * 1024
        for img in value:
            if img.size > max_size:
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
