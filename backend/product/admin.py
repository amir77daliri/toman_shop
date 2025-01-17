from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'owner')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]

    def owner(self, obj):
        if obj.owner:
            return f"{obj.owner.username}"
        return ""
    owner.short_description = 'owner'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product')
    list_filter = ('product',)
