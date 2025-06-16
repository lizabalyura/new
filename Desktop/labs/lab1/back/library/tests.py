from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Book, Genre


class BookGenreAPITest(APITestCase):
    def setUp(self):
        # Пользователи
        self.user = User.objects.create_user(username="user", password="pass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass", email="admin@example.com")

        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

        # Жанр
        self.genre = Genre.objects.create(name="Фантастика")

        # Книга
        self.book = Book.objects.create(title="Пример книги", author="Автор", description="описание")
        self.book.genre.set([self.genre])

        # Клиенты
        self.auth_client = APIClient()
        self.auth_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
    # --- КНИГИ ---
    def test_get_all_books(self):
        url = reverse('books')  # путь должен соответствовать твоему urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_book_authenticated(self):
        url = reverse('add_book')
        data = {'title': 'Новая книга', 'author': 'Новый автор','description':'описание', 'genre': self.genre.id}
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_book_unauthenticated(self):
        url = reverse('add_book')
        data = {'title': 'Новая книга', 'author': 'Новый автор', 'description':'описание', 'genre': self.genre.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_book(self):
        url = reverse('patch_book', kwargs={'id': self.book.id})
        data = {'title': 'Обновлённая книга'}
        response = self.auth_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Обновлённая книга')

    def test_put_book(self):
        url = reverse('put_book', kwargs={'id': self.book.id})
        data = {'title': 'Полная замена', 'author': 'Новый автор', 'description':'описание', 'genre': self.genre.id}
        response = self.auth_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_as_admin(self):
        url = reverse('delete_book', kwargs={'id': self.book.id})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_as_user(self):
        url = reverse('delete_book', kwargs={'id': self.book.id})
        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- ЖАНРЫ ---
    def test_get_all_genres(self):
        url = reverse('genres')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_genre(self):
        url = reverse('add_genre')
        data = {'name': 'Детектив'}
        response = self.auth_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_genre(self):
        url = reverse('put_genre', kwargs={'id': self.genre.id})
        data = {'name': 'Хоррор'}
        response = self.auth_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_genre_as_admin(self):
        url = reverse('delete_genre', kwargs={'id': self.genre.id})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_genre_as_user(self):
        url = reverse('delete_genre', kwargs={'id': self.genre.id})
        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- СОРТИРОВКА ---
    def test_book_list_filter_by_author(self):
        url = reverse('filter') + f'?author={self.book.author}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)