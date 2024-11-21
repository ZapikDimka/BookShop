from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookmarkViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
