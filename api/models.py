from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_genres = models.TextField(default="")
    movie_popularity = models.FloatField()
    movie_title = models.CharField(default="", max_length=50)
    movie_overview = models.TextField(default="")
    movie_vote_average = models.FloatField()


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    song_artist = models.CharField(default="", max_length=50)
    song_title = models.CharField(default="", max_length=50)
    song_text = models.TextField(default="")


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_authors = models.CharField(default="", max_length=100)
    book_title = models.CharField(default="", max_length=100)
    book_overview = models.TextField(default="")
    book_genres = models.TextField(default="")


class Movie_Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Book_Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Song_Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    rating = models.IntegerField()
