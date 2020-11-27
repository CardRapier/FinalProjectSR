
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Song, Movie, Book, Book_Rating, Movie_Rating, Song_Rating
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


class Recommendation_Songs():
    def __init__(self, songs, most_liked, songs_ratings, popular_songs):
        self.reader = Reader()
        self.svd = SVD()
        self.songs = songs
        self.most_liked = most_liked
        self.popular_songs = popular_songs
        self.songs_ratings = songs_ratings
        self.sim_cos_song = []
        self.indices = []
        self.data = []
        self.processing()
        self.processing_svd()

    def recommendate(self, id):
        populars = []
        recommendated = []
        for i in range(0, 3):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.most_liked) - 1)

            recommendated.append(ran)
            popular_song = self.most_liked[ran]
            song = Song(song_id=popular_song.song_id, song_title=popular_song.song_title,
                        song_artist=popular_song.song_artist, song_text=popular_song.song_text)
            populars.append(song)

        svd = self.SVDSong(id)
        populars.extend(svd)

        content = []
        for i in range(0, 6):
            recommendation = self.recommenderSong(
                1, getattr(svd[i], 'song_title'))
            content.extend(recommendation)
        populars.extend(content)

        return populars

    def recommendate_most_liked(self):
        most_liked = []
        recommendated = []
        for i in range(0, 20):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.most_liked) - 1)
            recommendated.append(ran)
            popular_song = self.most_liked[ran]
            song = Song(song_id=popular_song.song_id, song_title=popular_song.song_title,
                        song_artist=popular_song.song_artist, song_text=popular_song.song_text)
            most_liked.append(song)
        return most_liked

    def recommendate_populars(self):
        populars = []
        recommendated = []
        for i in range(0, 20):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.popular_songs) - 1)
            recommendated.append(ran)
            popular_song = self.popular_songs[ran]
            song = Song(song_id=popular_song.song_id, song_title=popular_song.song_title,
                        song_artist=popular_song.song_artist, song_text=popular_song.song_text)
            populars.append(song)
        return populars

    def processing(self):
        self.data = pd.DataFrame(
            map(lambda x: [x.song_artist, x.song_title, x.song_text, x.song_id], self.songs), columns=["song_artist", "song_title", "song_text", "song_id"])
        vectorizer1 = TfidfVectorizer(min_df=1, stop_words='english')
        self.data['song_text'] = self.data['song_text'].fillna('')
        bag_of_words_song = vectorizer1.fit_transform(self.data['song_text'])
        self.sim_cos_song = linear_kernel(bag_of_words_song, bag_of_words_song)
        self.indices = pd.Series(
            self.data.index, index=self.data['song_title']).drop_duplicates()

    def processing_svd(self):
        self.songs_ratings = pd.DataFrame(
            map(lambda x: [x.song_id_id, x.user_id_id, x.rating, x.id], self.songs_ratings), columns=["song_id", "user_id", "rating", "id"])
        self.songs_ratings.set_index('id', inplace=True)

    def recommenderSong(self, top, song):
        songs_to_recommendate = []
        idx = self.indices[song]
        ss = list(enumerate(self.sim_cos_song[idx]))
        ss = sorted(ss, key=lambda x: x[1], reverse=True)
        ss = ss[1:top+1]
        data_ind = [i[0] for i in ss]
        objec = self.data.iloc[data_ind].values.tolist()
        for i in objec:
            song = Song(song_id=i[3], song_title=i[1],
                        song_artist=i[0], song_text=i[2])
            songs_to_recommendate.append(song)
        return songs_to_recommendate

    def SVDSong(self, user_id):
        songs_to_recommendate = []
        data = Dataset.load_from_df(
            self.songs_ratings[['user_id', 'song_id', 'rating']][:], self.reader)

        df_user_to_recommend = self.songs_ratings[(
            self.songs_ratings['user_id'] == user_id) & (self.songs_ratings['rating'] >= 4)]

        df_user_to_recommend = df_user_to_recommend.set_index('song_id')
        df_user_to_recommend = df_user_to_recommend.join(self.data)[
            ['song_title', 'song_artist']]

        df_user_to_recommend = self.data.copy()
        df_user_to_recommend = df_user_to_recommend.reset_index()
        data = Dataset.load_from_df(
            self.songs_ratings[['user_id', 'song_id', 'rating']], self.reader)

        trainset = data.build_full_trainset()
        self.svd.fit(trainset)
        df_rated = self.songs_ratings[(
            self.songs_ratings['user_id'] == user_id)]
        df_rated = df_rated.set_index('song_id')
        df_rated = df_rated.join(self.data)[['song_title', 'song_artist']]

        df_user_to_recommend['Estimate_Score'] = df_user_to_recommend['song_id'].apply(
            lambda x: self.svd.predict(user_id, x).est)
        df_user_to_recommend = df_user_to_recommend[~df_user_to_recommend['song_title'].isin(
            df_rated['song_title'])]

        df_user_to_recommend = df_user_to_recommend.drop('song_id', axis=1)

        df_user_to_recommend = df_user_to_recommend.sort_values(
            'Estimate_Score', ascending=False)
        objec = df_user_to_recommend.head(11).values.tolist()
        for i in objec:
            song = Song(song_id=i[0]+1, song_title=i[2],
                        song_artist=i[1], song_text=i[3])
            songs_to_recommendate.append(song)
        return songs_to_recommendate
