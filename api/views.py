from django.shortcuts import render
from .serializers import SongSerializer, MovieSerializer, BookSerializer, Book_RatingSerializer, Movie_RatingSerializer, Song_RatingSerializer
from .models import Song, Movie, Book, Book_Rating, Movie_Rating, Song_Rating
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .recommendation_songs import Recommendation_Songs
from .recommendation_books import Recommendation_Books
from .recommendation_movies import Recommendation_Movies
# Create your views here.
from django.db import connection

max_value_songs = 0
with connection.cursor() as cursor:
    cursor.execute("SELECT MAX(rating) FROM api_song_rating")
    max_value_songs = cursor.fetchone()
songs = Song.objects.raw('SELECT api_song.* FROM api_song limit 4000')
songs_most_liked = Song.objects.raw(
    'SELECT api_song.*, SUM(api_song_rating.rating)/count(api_song_rating.rating) AS average FROM api_song, api_song_rating WHERE api_song.song_id=api_song_rating.song_id_id GROUP BY api_song.song_id ORDER BY average DESC')
song_by_popularity = Song.objects.raw(
    'SELECT api_song.*, ((SUM(api_song_rating.rating)/(COUNT(api_song_rating.rating))/%s)*5) AS coun FROM api_song, api_song_rating WHERE api_song.song_id = api_song_rating.song_id_id GROUP BY api_song.song_id ORDER BY coun DESC', [max_value_songs])
song_ratings = Song_Rating.objects.all()
recommendation_song = Recommendation_Songs(
    songs, songs_most_liked, song_ratings, song_by_popularity)

max_value_books = 0
with connection.cursor() as cursor:
    cursor.execute("SELECT MAX(rating) FROM api_book_rating")
    max_value_books = cursor.fetchone()
books = Book.objects.raw('SELECT * FROM api_book')
books_most_liked = Book.objects.raw(
    'SELECT api_book.*, SUM(api_book_rating.rating)/count(api_book_rating.rating) AS average FROM api_book, api_book_rating WHERE api_book.book_id=api_book_rating.book_id_id GROUP BY api_book.book_id ORDER BY average DESC')
book_by_popularity = Book.objects.raw(
    'SELECT api_book.*, ((SUM(api_book_rating.rating)/(COUNT(api_book_rating.rating))/%s)*5) AS coun FROM api_book, api_book_rating WHERE api_book.book_id=api_book_rating.book_id_id GROUP BY api_book.book_id ORDER BY coun DESC', [max_value_books])
books_ratings = Book_Rating.objects.all()
recommendation_book = Recommendation_Books(
    books, books_most_liked, books_ratings, book_by_popularity)

max_value_movies = 0
with connection.cursor() as cursor:
    cursor.execute("SELECT MAX(rating) FROM api_movie_rating")
    max_value_movies = cursor.fetchone()
movies = Movie.objects.raw('SELECT * FROM api_movie')
movies_most_liked = Movie.objects.raw(
    'SELECT api_movie.*, SUM(api_movie_rating.rating)/count(api_movie_rating.rating) AS average FROM api_movie, api_movie_rating WHERE api_movie.movie_id=api_movie_rating.movie_id_id GROUP BY api_movie.movie_id ORDER BY average DESC')
movie_by_popularity = Movie.objects.raw(
    'SELECT api_movie.*, ((SUM(api_movie_rating.rating)/(COUNT(api_movie_rating.rating))/%s)*5) AS coun FROM api_movie, api_movie_rating WHERE api_movie.movie_id=api_movie_rating.movie_id_id GROUP BY api_movie.movie_id ORDER BY coun DESC', [max_value_movies])
movies_ratings = Movie_Rating.objects.all()
recommendation_movie = Recommendation_Movies(
    movies, movies_most_liked, movies_ratings, movie_by_popularity)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'songs-routes': {
            'List': '/songs/',
            'Detail View': '/song/<str:pk>/',
            'Search': {'search/song/', 'body=search'},
            'Create': '/song-create/',
            'Update': '/song-update/<str:pk>/',
            'Delete': '/song-delete/<str:pk>/'
        },
        'movies-routes': {
            'List': '/movies/',
            'Detail View': '/movie/<str:pk>/',
            'Search': {'search/movie/', 'body=search'},
            'Create': '/movie-create/',
            'Update': '/movie-update/<str:pk>/',
            'Delete': '/movie-delete/<str:pk>/'
        },
        'books-routes': {
            'List': '/books/',
            'Detail View': '/book/<str:pk>/',
            'Search': {'search/book/', 'body=search'},
            'Create': '/book-create/',
            'Update': '/book-update/<str:pk>/',
            'Delete': '/book-delete/<str:pk>/'
        },
        'book_ratings-routes': {
            'List': '/book_ratings/',
            'Detail View': '/book_rating/<str:pk>/',
            'Create': '/book_rating-create/',
            'Update': '/book_rating-update/<str:pk>/',
            'Delete': '/book_rating-delete/<str:pk>/'
        },
        'movies_ratings-routes': {
            'List': '/movie_ratings/',
            'Detail View': '/movie_rating/<str:pk>/',
            'Create': '/movie_rating-create/',
            'Update': '/movie_rating-update/<str:pk>/',
            'Delete': '/movie_rating-delete/<str:pk>/'
        },
        'song_ratings-routes': {
            'List': '/song_ratings/',
            'Detail View': '/song_rating/<str:pk>/',
            'Create': '/song_rating-create/',
            'Update': '/song_rating-update/<str:pk>/',
            'Delete': '/song_rating-delete/<str:pk>/'
        }

    }

    return Response(api_urls)

##### Song End-Points ######


@api_view(['GET'])
def songList(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def songDetail(request, pk):
    songs = Song.objects.get(song_id=pk)
    serializer = SongSerializer(songs, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def songSearch(request):
    search = request.data['search']
    songs = Song.objects.raw(
        'SELECT * FROM api_song WHERE song_id < 4000 song_title REGEXP %s or song_artist REGEXP %s LIMIT 20', [search, search])
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def songCreate(request):
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def songUpdate(request, pk):
    song = Song.objects.get(song_id=pk)
    serializer = SongSerializer(instance=song, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def songDelete(request, pk):
    song = Song.objects.get(song_id=pk)
    song.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Movie End-Points ######


@api_view(['GET'])
def movieList(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def movieDetail(request, pk):
    movies = Movie.objects.get(movie_id=pk)
    serializer = MovieSerializer(movies, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def movieSearch(request):
    search = request.data['search']
    movies = Movie.objects.raw(
        'SELECT * FROM api_movie WHERE movie_title REGEXP %s LIMIT 20', [search])
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def movieCreate(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def movieUpdate(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    serializer = MovieSerializer(instance=movie, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def movieDelete(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    movie.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Book End-Points ######


@api_view(['GET'])
def bookList(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def bookDetail(request, pk):
    books = Book.objects.get(book_id=pk)
    serializer = BookSerializer(books, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def bookSearch(request):
    search = request.data['search']
    books = Book.objects.raw(
        'SELECT * FROM api_book WHERE book_title REGEXP %s or book_authors REGEXP %s LIMIT 20', [search, search])
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def bookCreate(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bookUpdate(request, pk):
    book = Book.objects.get(book_id=pk)
    serializer = BookSerializer(instance=book, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def bookDelete(request, pk):
    book = Book.objects.get(book_id=pk)
    book.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Book Rating End-Points ######


@api_view(['GET'])
def book_ratingList(request):
    ratings = Book_Rating.objects.all()
    serializer = Book_RatingSerializer(ratings, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def book_ratingDetail(request,  pk, pk2):
    rating = Book_Rating.objects.get(user_id=pk, book_id=pk2)
    serializer = Book_RatingSerializer(rating, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def book_ratingCreate(request):
    serializer = Book_RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def book_ratingUpdate(request,  pk, pk2):
    rating = Book_Rating.objects.get(user_id=pk, book_id=pk2)
    serializer = Book_RatingSerializer(instance=rating, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def book_ratingDelete(request, pk):
    rating = Book_Rating.objects.get(id=pk)
    rating.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Movie Rating End-Points ######


@api_view(['GET'])
def movie_ratingList(request):
    ratings = Movie_Rating.objects.all()
    serializer = Movie_RatingSerializer(ratings, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def movie_ratingDetail(request,  pk, pk2):
    rating = Movie_Rating.objects.get(user_id=pk, movie_id=pk2)
    serializer = Movie_RatingSerializer(rating, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def movie_ratingCreate(request):
    serializer = Movie_RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def movie_ratingUpdate(request,  pk, pk2):
    rating = Movie_Rating.objects.get(user_id=pk, movie_id=pk2)
    serializer = Movie_RatingSerializer(instance=rating, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def movie_ratingDelete(request, pk):
    rating = Movie_Rating.objects.get(id=pk)
    rating.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Song Rating End-Points ######


@api_view(['GET'])
def song_ratingList(request):
    ratings = Song_Rating.objects.all()
    serializer = Song_RatingSerializer(ratings, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def song_ratingDetail(request, pk, pk2):
    rating = Song_Rating.objects.get(user_id=pk, song_id=pk2)
    serializer = Song_RatingSerializer(rating, many=False)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def song_ratingCreate(request):
    serializer = Song_RatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def song_ratingUpdate(request, pk, pk2):
    rating = Song_Rating.objects.get(user_id=pk, song_id=pk2)
    serializer = Song_RatingSerializer(instance=rating, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def song_ratingDelete(request, pk):
    rating = Song_Rating.objects.get(id=pk)
    rating.delete()

    return Response("Has been deleted succesfuly", status.HTTP_200_OK)

##### Song Recommendation End-Points ######


@api_view(['POST'])
def song_recommendation(request):
    id = request.data['id']
    recommendation = recommendation_song.recommendate(id)
    serializer = SongSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def song_recommendation_populars(request):
    recommendation = recommendation_song.recommendate_populars()
    serializer = SongSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def song_recommendation_most_liked(request):
    recommendation = recommendation_song.recommendate_most_liked()
    serializer = SongSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

##### Book Recommendation End-Points ######


@api_view(['POST'])
def book_recommendation(request):
    #id = request.data['id']
    recommendation = recommendation_book.recommendate(1)
    serializer = BookSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def book_recommendation_populars(request):
    recommendation = recommendation_book.recommendate_populars()
    serializer = BookSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def book_recommendation_most_liked(request):
    recommendation = recommendation_book.recommendate_most_liked()
    serializer = BookSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

##### Movie Recommendation End-Points ######


@api_view(['POST'])
def movie_recommendation(request):
    id = request.data['id']
    recommendation = recommendation_movie.recommendate(id)
    serializer = MovieSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def movie_recommendation_populars(request):
    recommendation = recommendation_movie.recommendate_populars()
    serializer = MovieSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def movie_recommendation_most_liked(request):
    recommendation = recommendation_movie.recommendate_most_liked()
    serializer = MovieSerializer(recommendation, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
