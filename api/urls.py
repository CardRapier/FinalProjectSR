from django.urls import path
from . import views

urlpatterns = [

    path('', views.apiOverview, name="api-overview"),

    ### Songs URLS ###
    path('songs/', views.songList, name="songs"),
    path('song/<str:pk>/', views.songDetail, name="song-detail"),
    path('song-create/', views.songCreate, name="song-create"),
    path('song-update/<str:pk>/', views.songUpdate, name="song-update"),
    path('song-delete/<str:pk>/', views.songDelete, name="song-delete"),

    ### Movie URLS ###
    path('movies/', views.movieList, name="movies"),
    path('movie/<str:pk>/', views.movieDetail, name="movie-detail"),
    path('movie-create/', views.movieCreate, name="movie-create"),
    path('movie-update/<str:pk>/', views.movieUpdate, name="movie-update"),
    path('movie-delete/<str:pk>/', views.movieDelete, name="movie-delete"),

    ### Book URLS ###
    path('books/', views.bookList, name="books"),
    path('book/<str:pk>/', views.bookDetail, name="book-detail"),
    path('book-create/', views.bookCreate, name="book-create"),
    path('book-update/<str:pk>/', views.bookUpdate, name="book-update"),
    path('book-delete/<str:pk>/', views.bookDelete, name="book-delete"),

    ### Book Rating URLS ###
    path('book_ratings/', views.book_ratingList, name="book_ratings"),
    path('book_rating/<str:pk>/', views.book_ratingDetail,
         name="book_rating-detail"),
    path('book_rating-create/', views.book_ratingCreate,
         name="book_rating-create"),
    path('book_rating-update/<str:pk>/',
         views.book_ratingUpdate, name="book_rating-update"),
    path('book_rating-delete/<str:pk>/',
         views.book_ratingDelete, name="book_rating-delete"),

    ### Movie Rating URLS ###
    path('movie_ratings/', views.movie_ratingList, name="movie_ratings"),
    path('movie_rating/<str:pk>/', views.movie_ratingDetail,
         name="movie_rating-detail"),
    path('movie_rating-create/', views.movie_ratingCreate,
         name="movie_rating-create"),
    path('movie_rating-update/<str:pk>/',
         views.movie_ratingUpdate, name="movie_rating-update"),
    path('movie_rating-delete/<str:pk>/',
         views.movie_ratingDelete, name="movie_rating-delete"),

    ### Song Rating URLS ###
    path('song_ratings/', views.song_ratingList, name="song_ratings"),
    path('song_rating/<str:pk>/', views.song_ratingDetail,
         name="song_rating-detail"),
    path('song_rating-create/', views.song_ratingCreate,
         name="song_rating-create"),
    path('song_rating-update/<str:pk>/',
         views.song_ratingUpdate, name="song_rating-update"),
    path('song_rating-delete/<str:pk>/',
         views.song_ratingDelete, name="song_rating-delete"),

    # Recomendatinos
    path('recomendation/songs/',
         views.song_recomendation, name="songs_recomendation"),
]
