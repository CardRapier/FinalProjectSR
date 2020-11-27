import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie, Movie_Rating
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


class Recommendation_Movies():
    def __init__(self, movies, most_liked, movies_ratings, popular_movies):
        self.reader = Reader()
        self.svd = SVD()
        self.movies = movies
        self.most_liked = most_liked
        self.popular_movies = popular_movies
        self.movies_ratings = movies_ratings
        self.sim_cos_movie = []
        self.indices = []
        self.data = []
        self.processing()
        self.processing_svd()

    def recommendate(self, id):
        populars = []
        recommendated = []
        for i in range(0, 1):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.most_liked) - 1)

            recommendated.append(ran)
            popular_movie = self.most_liked[ran]
            movie = Movie(movie_id=popular_movie.movie_id, movie_title=popular_movie.movie_title,
                          movie_overview=popular_movie.movie_overview, movie_genres=popular_movie.movie_genres)
            populars.append(movie)

        content = []
        for i in populars:
            recommendation = self.recommenderMovie(
                2, getattr(i, 'movie_title'))
            content.extend(recommendation)
        populars.extend(content)
        populars.extend(self.SVDMovie(id))

        return populars

    def recommendate_most_liked(self):
        most_liked = []
        recommendated = []
        for i in range(0, 3):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.most_liked) - 1)
            recommendated.append(ran)
            popular_movie = self.most_liked[ran]
            movie = Movie(movie_id=popular_movie.movie_id, movie_title=popular_movie.movie_title,
                          movie_overview=popular_movie.movie_overview, movie_genres=popular_movie.movie_genres)
            most_liked.append(movie)
        return most_liked

    def recommendate_populars(self):
        populars = []
        recommendated = []
        for i in range(0, len(self.popular_movies)):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.popular_movies) - 1)
            recommendated.append(ran)
            popular_movie = self.popular_movies[ran]
            movie = Movie(movie_id=popular_movie.movie_id, movie_title=popular_movie.movie_title,
                          movie_overview=popular_movie.movie_overview, movie_genres=popular_movie.movie_genres)
            populars.append(movie)
        return populars

    def processing(self):
        self.data = pd.DataFrame(
            map(lambda x: [x.movie_title, x.movie_overview, x.movie_id, x.movie_genres], self.movies), columns=["movie_title", "movie_overview", "movie_id", "movie_genres"])
        vectorizer1 = TfidfVectorizer(min_df=1, stop_words='english')
        self.data['movie_overview'] = self.data['movie_overview'].fillna('')
        bag_of_words_movie = vectorizer1.fit_transform(
            self.data['movie_overview'])
        self.sim_cos_movie = linear_kernel(
            bag_of_words_movie, bag_of_words_movie)
        self.indices = pd.Series(
            self.data.index, index=self.data['movie_title']).drop_duplicates()

    def processing_svd(self):
        self.movies_ratings = pd.DataFrame(
            map(lambda x: [x.movie_id_id, x.user_id_id, x.rating, x.id], self.movies_ratings), columns=["movie_id", "user_id", "rating", "id"])
        self.movies_ratings.set_index('id', inplace=True)

    def recommenderMovie(self, top, movie):
        movies_to_recommendate = []
        idx = self.indices[movie]
        ss = list(enumerate(self.sim_cos_movie[idx]))
        ss = sorted(ss, key=lambda x: x[1], reverse=True)
        ss = ss[1:top+1]
        data_ind = [i[0] for i in ss]
        objec = self.data.iloc[data_ind].values.tolist()
        for i in objec:
            movie = Movie(movie_id=i[2], movie_title=i[0],
                          movie_overview=i[1], movie_genres=i[3])
            movies_to_recommendate.append(movie)
        return movies_to_recommendate

    def SVDMovie(self, user_id):
        movies_to_recommendate = []
        data = Dataset.load_from_df(
            self.movies_ratings[['user_id', 'movie_id', 'rating']][:], self.reader)

        df_user_to_recommend = self.movies_ratings[(
            self.movies_ratings['user_id'] == user_id) & (self.movies_ratings['rating'] >= 4)]

        df_user_to_recommend = df_user_to_recommend.set_index('movie_id')
        df_user_to_recommend = df_user_to_recommend.join(self.data)[
            ['movie_title']]

        df_user_to_recommend = self.data.copy()
        df_user_to_recommend = df_user_to_recommend.reset_index()
        data = Dataset.load_from_df(
            self.movies_ratings[['user_id', 'movie_id', 'rating']], self.reader)

        trainset = data.build_full_trainset()
        self.svd.fit(trainset)
        df_rated = self.movies_ratings[(
            self.movies_ratings['user_id'] == user_id)]
        df_rated = df_rated.set_index('movie_id')
        df_rated = df_rated.join(self.data)[['movie_title']]
        df_user_to_recommend['Estimate_Score'] = df_user_to_recommend['movie_id'].apply(
            lambda x: self.svd.predict(user_id, x).est)
        df_user_to_recommend = df_user_to_recommend[~df_user_to_recommend['movie_title'].isin(
            df_rated['movie_title'])]

        df_user_to_recommend = df_user_to_recommend.drop('movie_id', axis=1)

        df_user_to_recommend = df_user_to_recommend.sort_values(
            'Estimate_Score', ascending=False)
        objec = df_user_to_recommend.head(11).values.tolist()
        for i in objec:
            movie = Movie(movie_id=i[0]+1, movie_title=i[1],
                          movie_overview=i[2], movie_genres=i[3])
            movies_to_recommendate.append(movie)
        return movies_to_recommendate
