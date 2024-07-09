from django.urls import path
from .views import ProductListCreateApiView, ProductRetrieveUpdateDestroyApiView

urlpatterns = [
    path('', ProductListCreateApiView.as_view(), name='product_list_create'),
    path('<int:pk>', ProductRetrieveUpdateDestroyApiView.as_view(), name='product_detail'),
]

