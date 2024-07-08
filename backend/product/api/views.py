from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductSerializer
from product.models import Product


class ProductListCreateApiView(generics.ListCreateAPIView):
    class ProductPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 20

    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return Product.objects.prefetch_related('images')

    def post(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                ser_data.save()
        except Exception as e:
            return Response(
                {'msg': 'Failed to save data', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(ser_data.data, status=status.HTTP_201_CREATED)
