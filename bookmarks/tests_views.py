from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase

from bookmarks.models import Category, Bookmark

# Отримання кастомної моделі користувача
User = get_user_model()


class APITests(APITestCase):
    def setUp(self):
        # Створення користувача для аутентифікації з кастомною моделлю
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Створення категорії для тестів
        self.category = Category.objects.create(name='Test Category', user=self.user)

    # Тест на отримання всіх закладок
    def test_get_all_bookmarks(self):
        response = self.client.get(reverse('bookmark-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тест на створення нової закладки
    def test_create_bookmark(self):
        data = {
            'title': 'New Bookmark',
            'url': 'https://example.com',
            'category_id': self.category.id,
            'favorite': False,
        }
        response = self.client.post(reverse('bookmark-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Негативний тест: спроба створення закладки без назви
    def test_create_bookmark_without_title(self):
        data = {
            'url': 'https://example.com',
            'category_id': self.category.id,
            'favorite': False,
        }
        response = self.client.post(reverse('bookmark-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Негативний тест: спроба видалення закладки іншим користувачем
    def test_delete_bookmark_by_other_user(self):
        new_user = User.objects.create_user(username='otheruser', email='otheruser@example.com', password='otherpass')
        other_client = APIClient()
        other_client.force_authenticate(user=new_user)

        # Створюємо закладку, яку створив основний користувач
        bookmark = Bookmark.objects.create(
            title='Other User Bookmark',
            url='https://example.com',
            category=self.category,
            user=self.user
        )

        # Інший користувач намагається видалити закладку
        response = other_client.delete(reverse('bookmark-detail', args=[bookmark.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Тест на отримання всіх категорій
    def test_get_all_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тест на створення нової категорії
    def test_create_category(self):
        data = {'name': 'New Category'}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Негативний тест: створення категорії з уже існуючою назвою
    def test_create_category_with_existing_name(self):
        data = {'name': 'Test Category'}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Тест на отримання токена JWT
    def test_get_jwt_token(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    # Негативний тест: спроба отримання токена з невірним паролем
    def test_get_jwt_token_with_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HTMLPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    # Тест на головну сторінку
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    # Тест на сторінку закладок
    def test_bookmarks_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 200)

    # Тест на сторінку категорій
    def test_categories_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    # Тест на сторінку улюблених
    def test_favorites_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)

    # Тест на сторінку пошуку
    def test_search_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)


class UserAuthTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        self.user = User.objects.create_user(**self.user_data)

    # Тест на реєстрацію
    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Перенаправлення після реєстрації

    # Тест на логін
    def test_login_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Перенаправлення після логіну

    # Тест на логін з неправильним паролем
    def test_login_with_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)  # Відображення форми з помилкою

    # Тест на вихід з системи
    def test_logout_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Перенаправлення після виходу
