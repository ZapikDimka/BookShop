from django.contrib import admin
from django.urls import path, include
from .views import home  # Імпортуємо view для головної сторінки
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),  # Панель адміністратора
    path('api/', include('bookmarks.urls')),  # API для закладок
    path('', home, name='home'),  # Головна сторінка
    path('bookmarks/', TemplateView.as_view(template_name='bookmarks.html'), name='bookmarks'),  # Закладки
    path('categories/', TemplateView.as_view(template_name='categories.html'), name='categories'),  # Категорії
    path('favorites/', TemplateView.as_view(template_name='favorites.html'), name='favorites'),  # Улюблені
    path('search/', TemplateView.as_view(template_name='search.html'), name='search'),  # Пошук
]
