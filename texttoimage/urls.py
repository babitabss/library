from django.urls import path
from .views import image_page, generate_image

urlpatterns = [
    path("image/", image_page, name="image_page"),
    path("generate/", generate_image, name="generate_image"),
]
