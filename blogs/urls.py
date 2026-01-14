from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewset, CategoryViewset, PostViewset, CommentViewset



router = routers.DefaultRouter()
router.register(r'author', AuthorViewset)
router.register(r'post', PostViewset)
router.register(r'category', CategoryViewset)
router.register(r'comment', CommentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
   
]
