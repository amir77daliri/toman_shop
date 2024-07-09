from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductCreateSerializer, ProductUpdateSerializer
from product.models import Product


class ProductListCreateApiView(generics.ListCreateAPIView):
    """
    API view to retrieve list of products or create a new product.
    required authentication for product creation
    use transaction to save product and its related images
    """

    class ProductPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 20

    serializer_class = ProductCreateSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.prefetch_related('images')

    def post(self, request, *args, **kwargs):
        context = super().get_serializer_context()
        ser_data = self.serializer_class(data=request.data, context=context)
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


class ProductRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """
        API view to retrieve-update-destroy A product.
        required authentication for product update / delete
        use transaction to save product and its related images
    """

    serializer_class = ProductUpdateSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        product = get_object_or_404(Product.objects.prefetch_related('images'), id=pk)
        return product

    def update(self, request, *args, **kwargs):
        pass
