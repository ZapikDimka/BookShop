from rest_framework import serializers
from .models import Bookmark, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Поля, які будуть передаватись

class BookmarkSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Використовуємо CategorySerializer для відображення категорії
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)  # Для передачі категорії по ID

    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'url', 'category', 'category_id', 'favorite']  # Включаємо категорію і category_id для створення
