
import random
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Book, Movie, Book, Book_Rating, Movie_Rating, Book_Rating
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


class Recommendation_Books():
    def __init__(self, books, most_liked, books_ratings, popular_books):
        self.reader = Reader()
        self.svd = SVD()
        self.books = books
        self.most_liked = most_liked
        self.popular_books = popular_books
        self.books_ratings = books_ratings
        self.sim_cos_book = []
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
            popular_book = self.most_liked[ran]
            book = Book(book_id=popular_book.book_id, book_title=popular_book.book_title,
                        book_authors=popular_book.book_authors, book_overview=popular_book.book_overview, book_genres=popular_book.book_genres)
            populars.append(book)

        content = []
        for i in populars:
            recommendation = self.recommenderBook(2, getattr(i, 'book_title'))
            content.extend(recommendation)
        populars.extend(content)
        populars.extend(self.SVDBook(id))

        return populars

    def recommendate_most_liked(self):
        most_liked = []
        recommendated = []
        for i in range(0, len(self.most_liked)):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.most_liked) - 1)
            recommendated.append(ran)
            popular_book = self.most_liked[ran]
            book = Book(book_id=popular_book.book_id, book_title=popular_book.book_title,
                        book_authors=popular_book.book_authors, book_overview=popular_book.book_overview, book_genres=popular_book.book_genres)
            most_liked.append(book)
        return most_liked

    def recommendate_populars(self):
        populars = []
        recommendated = []
        for i in range(0, len(self.popular_books)):
            ran = 0
            while (ran in recommendated):
                ran = random.randint(0, len(self.popular_books) - 1)
            recommendated.append(ran)
            popular_book = self.popular_books[ran]
            book = Book(book_id=popular_book.book_id, book_title=popular_book.book_title,
                        book_authors=popular_book.book_authors, book_overview=popular_book.book_overview, book_genres=popular_book.book_genres)
            populars.append(book)
        return populars

    def processing(self):
        self.data = pd.DataFrame(
            map(lambda x: [x.book_authors, x.book_title, x.book_overview, x.book_id, x.book_genres], self.books), columns=["book_authors", "book_title", "book_overview", "book_id", "book_genres"])
        vectorizer1 = TfidfVectorizer(min_df=1, stop_words='english')
        self.data['book_overview'] = self.data['book_overview'].fillna('')
        bag_of_words_book = vectorizer1.fit_transform(
            self.data['book_overview'])
        self.sim_cos_book = linear_kernel(bag_of_words_book, bag_of_words_book)
        self.indices = pd.Series(
            self.data.index, index=self.data['book_title']).drop_duplicates()

    def processing_svd(self):
        self.books_ratings = pd.DataFrame(
            map(lambda x: [x.book_id_id, x.user_id_id, x.rating, x.id], self.books_ratings), columns=["book_id", "user_id", "rating", "id"])
        self.books_ratings.set_index('id', inplace=True)

    def recommenderBook(self, top, book):
        books_to_recommendate = []
        idx = self.indices[book]
        ss = list(enumerate(self.sim_cos_book[idx]))
        ss = sorted(ss, key=lambda x: x[1], reverse=True)
        ss = ss[1:top+1]
        data_ind = [i[0] for i in ss]
        objec = self.data.iloc[data_ind].values.tolist()
        for i in objec:
            book = Book(book_id=i[3], book_title=i[1],
                        book_authors=i[0], book_overview=i[2], book_genres=i[4])
            books_to_recommendate.append(book)
        return books_to_recommendate

    def SVDBook(self, user_id):
        books_to_recommendate = []
        data = Dataset.load_from_df(
            self.books_ratings[['user_id', 'book_id', 'rating']][:], self.reader)

        df_user_to_recommend = self.books_ratings[(
            self.books_ratings['user_id'] == user_id) & (self.books_ratings['rating'] >= 4)]

        df_user_to_recommend = df_user_to_recommend.set_index('book_id')
        df_user_to_recommend = df_user_to_recommend.join(self.data)[
            ['book_title', 'book_authors']]

        df_user_to_recommend = self.data.copy()
        df_user_to_recommend = df_user_to_recommend.reset_index()
        data = Dataset.load_from_df(
            self.books_ratings[['user_id', 'book_id', 'rating']], self.reader)

        trainset = data.build_full_trainset()
        self.svd.fit(trainset)
        df_rated = self.books_ratings[(
            self.books_ratings['user_id'] == user_id)]
        df_rated = df_rated.set_index('book_id')
        df_rated = df_rated.join(self.data)[['book_title', 'book_authors']]
        df_user_to_recommend['Estimate_Score'] = df_user_to_recommend['book_id'].apply(
            lambda x: self.svd.predict(user_id, x).est)
        df_user_to_recommend = df_user_to_recommend[~df_user_to_recommend['book_title'].isin(
            df_rated['book_title'])]

        df_user_to_recommend = df_user_to_recommend.drop('book_id', axis=1)

        df_user_to_recommend = df_user_to_recommend.sort_values(
            'Estimate_Score', ascending=False)
        objec = df_user_to_recommend.head(11).values.tolist()
        for i in objec:
            book = Book(book_id=i[0]+1, book_title=i[2],
                        book_authors=i[1], book_overview=i[3], book_genres=i[4])
            books_to_recommendate.append(book)
        return books_to_recommendate
