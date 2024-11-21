from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Bookmark, Category
from .serializers import BookmarkSerializer, CategorySerializer


# Bookmark ViewSet (для API доступу до закладок)
class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'favorite']
    search_fields = ['title', 'url']

    def get_queryset(self):
        # Фільтруємо закладки за поточним користувачем
        return Bookmark.objects.filter(user=self.request.user).order_by('title')

    def perform_create(self, serializer):
        # Автоматично встановлюємо користувача як власника закладки
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Логування даних запиту
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Логування помилок
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def favorite(self, request, pk=None):
        bookmark = self.get_object()
        bookmark.favorite = not bookmark.favorite
        bookmark.save()
        return Response({'status': 'favorite updated'}, status=status.HTTP_200_OK)


# Category ViewSet (для API доступу до категорій)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Фільтруємо категорії за поточним користувачем
        return Category.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        # Автоматично встановлюємо користувача як власника категорії
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')

        # Перевірка, чи існує категорія з таким іменем у поточного користувача
        if Category.objects.filter(name=name, user=request.user).exists():
            return Response(
                {"error": "A category with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Логування помилок
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Функціональні подання для рендерингу HTML
@login_required
def bookmarks_view(request):
    return render(request, 'bookmarks.html')


@login_required
def categories_view(request):
    return render(request, 'categories.html')


@login_required
def favorites_view(request):
    return render(request, 'favorites.html')


@login_required
def search_view(request):
    return render(request, 'search.html')
