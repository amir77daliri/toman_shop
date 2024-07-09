from django.urls import path
from .views import ProductListCreateApiView, ProductRetrieveUpdateDestroyApiView

urlpatterns = [
    path('', ProductListCreateApiView.as_view()),
    path('<int:pk>', ProductRetrieveUpdateDestroyApiView.as_view()),
]

