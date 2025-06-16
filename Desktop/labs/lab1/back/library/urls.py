from django.urls import path
from .views import *
urlpatterns = [
    path('books/', get_all_books, name="books"),
    path('add_book/', post_book, name="add_book"),
    path('put_book/<int:id>', put_book, name="put_book"),
    path('patch_book/<int:id>', patch_book, name="patch_book"),
    path('delete_book/<int:id>', delete_book, name="delete_book"),


    path('genres/', get_all_genres, name="genres"),
    path('add_genre/', post_genre, name="add_genre"),
    path('put_genre/<int:id>', put_genre, name="put_genre"),
    path('delete_genre/<int:id>', delete_genre, name="delete_genre"),

    path('filter/', BookListView.as_view(), name="filter"),
]