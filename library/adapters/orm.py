from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey,Boolean,Text
)
from sqlalchemy.orm import mapper, relationship
from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('user_name', String(255), primary_key=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('want_to_read', Text, nullable=True)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', String(255), nullable=False),
    Column('book_id', ForeignKey('books.book_id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', Date, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('release_year', Integer, nullable=True),
    Column('ebook', Boolean(), nullable=True),
    Column('num_pages', Integer, nullable=True)
)

authors_table = Table(
    'authors', metadata,
    Column('unique_id', Integer, primary_key=True),
    Column('full_name', String(255), nullable=True)
)

book_author_table = Table(
    'book_author', metadata,
    Column('book_id', ForeignKey('books.book_id'), primary_key=True),
    Column('author_id', ForeignKey('authors.unique_id'), primary_key=True)
)

publisher_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)

def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__want_to_read': users_table.c.want_to_read
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__user': reviews_table.c.user,
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__book': relationship(model.Book)
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__publisher': relationship(model.Publisher),
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__authors': relationship(model.Author, secondary=book_author_table, lazy='select')
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.unique_id,
        '_Author__full_name': authors_table.c.full_name,
    })

    mapper(model.Publisher, publisher_table, properties={
        '_Publisher__name': publisher_table.c.name
    })

