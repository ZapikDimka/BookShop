from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from bookmarks.views import bookmarks_view, categories_view, favorites_view, search_view
from django.contrib.auth.decorators import login_required
from .views import home  # Імпортуємо view для головної сторінки

urlpatterns = [
    path('admin/', admin.site.urls),  # Панель адміністратора
    path('api/', include('bookmarks.urls')),  # API для закладок
    path('', home, name='home'),  # Головна сторінка

    # Додаємо login_required до сторінок, які потребують авторизації
    path('bookmarks/', login_required(bookmarks_view), name='bookmarks'),  # Закладки
    path('categories/', login_required(categories_view), name='categories'),  # Категорії
    path('favorites/', login_required(favorites_view), name='favorites'),  # Улюблені
    path('search/', login_required(search_view), name='search'),  # Пошук

    path('users/', include('users.urls')),  # URL для реєстрації, логіну і логауту

    # JWT токени
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
