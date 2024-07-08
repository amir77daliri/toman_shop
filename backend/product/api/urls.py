from django.urls import path
from .views import ProductListCreateApiView

urlpatterns = [
    path('', ProductListCreateApiView.as_view()),
]

