
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Song, Movie, Book, Book_Rating, Movie_Rating, Song_Rating


class Recommendation_Songs():
    def __init__(self, songs, popular_songs, songs_ratings):
        self.songs = songs
        self.popular_songs = popular_songs
        self.songs_ratings = songs_ratings
        self.sim_cos_song = []
        self.indices = []
        self.data = []
        self.processing()

    def recommendate(self):
        populars = []
        recommendated = []
        for i in range(0, 3):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.popular_songs) - 1)
            recommendated.append(ran)
            popular_song = self.popular_songs[ran]
            song = Song(song_id=popular_song.song_id, song_title=popular_song.song_title,
                        song_artist=popular_song.song_artist, song_text=popular_song.song_text)
            populars.append(song)

        for i in range(len(populars)):
            populars.extend(self.recommenderSong(1, populars[i].song_title))
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
        print(self.data.index, 'index')

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
