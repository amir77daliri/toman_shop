from django.urls import path
from .views import RegisterApiView, LoginApiView


urlpatterns = [
    path('login/', LoginApiView.as_view()),
    path('register/', RegisterApiView.as_view()),
]

