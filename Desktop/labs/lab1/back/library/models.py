from django.db import models

# Описание модели книги и жанров

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=200)
    genre = models.ManyToManyField('Genre') # отложенная ссылка на всякий случай

    def __str__(self):
        return self.name