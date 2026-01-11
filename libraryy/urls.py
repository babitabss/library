from django.urls import path, include
from .views import BookViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
