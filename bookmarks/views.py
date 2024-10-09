from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Bookmark, Category
from .serializers import BookmarkSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

# Bookmark ViewSet
class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all().order_by('title')  # Сортуємо закладки за назвою
    serializer_class = BookmarkSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'favorite']
    search_fields = ['title', 'url']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        title = request.data.get('title')
        category_id = request.data.get('category')

        # Перевіряємо чи існує закладка з такою ж URL та назвою
        if Bookmark.objects.filter(url=url, title=title).exists():
            return Response(
                {"error": "A bookmark with this URL and title already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Перевіряємо чи існує закладка з такою ж URL
        if Bookmark.objects.filter(url=url).exists():
            return Response(
                {"error": "A bookmark with this URL already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Перевіряємо чи існує закладка з такою ж назвою
        if Bookmark.objects.filter(title=title).exists():
            return Response(
                {"error": "A bookmark with this title already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Отримуємо категорію, якщо вона вказана
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            category = None

        # Створюємо закладку
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)  # Прив'язуємо категорію до закладки
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def favorite(self, request, pk=None):
        # Зміна статусу "улюблене"
        bookmark = self.get_object()
        bookmark.favorite = not bookmark.favorite
        bookmark.save()
        return Response({'status': 'favorite updated'}, status=status.HTTP_200_OK)


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')  # Сортуємо категорії за назвою
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')

        # Перевіряємо чи існує категорія з такою ж назвою
        if Category.objects.filter(name=name).exists():
            return Response(
                {"error": "A category with this name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
