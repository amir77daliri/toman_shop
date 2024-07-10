from django.contrib.auth import get_user_model
from rest_framework import serializers
from product.models import Product, ProductImage
from decouple import config

MAX_IMG_SIZE = config('MAX_IMG_SIZE', cast=int, default=2097152)
MAX_IMG_PER_PRODUCT = (config('MAX_ING_PER_PRODUCT', cast=int, default=5))


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductBaseSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    new_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def validate_new_images(self, value):
        if len(value) > MAX_IMG_PER_PRODUCT:
            raise serializers.ValidationError(f"Only up to {MAX_IMG_PER_PRODUCT} image could post per product")

        for img in value:
            if img.size > MAX_IMG_SIZE:
                raise serializers.ValidationError(f"image {img} is over 2MB")
        return value

    def create_images(self, product, new_images):
        for img in new_images:
            ProductImage.objects.create(product=product, image=img)


class ProductCreateSerializer(ProductBaseSerializer):

    def create(self, validated_data):
        new_images = validated_data.pop('new_images', [])
        owner = self.context['request'].user
        product = Product.objects.create(**validated_data, owner=owner)
        self.create_images(product, new_images)
        return product


class ProductUpdateSerializer(ProductBaseSerializer):
    old_images_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)

        if 'old_images_ids' not in validated_attrs:
            raise serializers.ValidationError("old_images_ids field is required.")
        new_images_count = len(validated_attrs.get('new_images', []))
        if new_images_count + len(validated_attrs['old_images_ids']) > MAX_IMG_PER_PRODUCT:
            raise serializers.ValidationError(f"Only up to {MAX_IMG_PER_PRODUCT} image could post per product")
        return validated_attrs

    def update(self, instance, validated_data):
        old_imgs_ids = validated_data.pop('old_images_ids', [])
        instance_images_ids = instance.images.values_list('id', flat=True)
        removed_ids = [i for i in list(instance_images_ids) if i not in old_imgs_ids]
        # remove old images that are deleted by client :
        instance.images.filter(id__in=removed_ids).delete()
        # Set new values if provided:
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)

        instance.save()

        # Add new images:
        self.create_images(instance, validated_data.get('new_images', []))

        return instance
