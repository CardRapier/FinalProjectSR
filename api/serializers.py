from rest_framework import serializers
from . import models


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class Movie_RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie_Rating
        fields = '__all__'


class Song_RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song_Rating
        fields = '__all__'


class Book_RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book_Rating
        fields = '__all__'
