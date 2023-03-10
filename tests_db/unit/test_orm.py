import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import *

article_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    rows = list(empty_session.execute('SELECT * from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT * from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (book_id, title, description, publisher_name, release_year,ebook,num_pages) VALUES '
        '(1,"test","desc", "test_pub", 2021, 1, 122)')

    empty_session.execute(
        'INSERT INTO authors (unique_id, full_name) VALUES '
        '(1, "test_author")')

    empty_session.execute(
        'INSERT INTO book_author (book_id, author_id) VALUES '
        '(1, 1)')

    empty_session.execute(
        'INSERT INTO publishers (name) VALUES '
        '("test_pub")')
    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def insert_review(empty_session):
    empty_session.execute(
        'INSERT INTO reviews (id, user, book_id, review_text, rating,timestamp) VALUES '
        '(1,"Andrew",1,"Good",5,"2021-10-13")')

    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]

def make_user():
    user = User("Andrew", "12341234")
    return user

def make_book():
    book = Book(2,"test_book")
    return book

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "12341234"))
    users.append(("cindy", "43214321"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "12341234"),
        User("cindy", "43214321")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "12341234")]

def test_loading_of_book(empty_session):
    article_key = insert_book(empty_session)
    fetched_book = empty_session.query(Book).one()

    assert article_key == fetched_book.book_id

def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT book_id, title FROM books'))
    assert rows == [(2, "test_book")]

def test_loading_of_author(empty_session):
    insert_book(empty_session)
    fetched_book = empty_session.query(Book).one()

    assert "test_author" == fetched_book.authors[0].full_name
    
def test_saving_of_author(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()
    fetched_book = empty_session.query(Book).one()
    fetched_book.add_author(Author(2,"a_n"))
    assert "a_n" == fetched_book.authors[0].full_name

def test_loading_of_publisher(empty_session):
    insert_book(empty_session)
    fetched_book = empty_session.query(Book).one()

    assert "test_pub" == fetched_book.publisher.name

def test_saving_of_publisher(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()
    fetched_book = empty_session.query(Book).one()
    fetched_book.publisher = Publisher("t_pub")
    assert "t_pub" == fetched_book.publisher.name

def test_loading_of_review(empty_session):
    insert_user(empty_session, ("Andrew", "12341234"))
    insert_book(empty_session)
    insert_review(empty_session)
    fetched_book = empty_session.query(Review).one()

    assert "Good" == fetched_book.review_text

def test_saving_of_review(empty_session):
    insert_user(empty_session, ("Andrew", "12341234"))
    insert_book(empty_session)
    book = empty_session.query(Book).one()
    empty_session.add(Review(book,"Good",5,"Andrew"))
    empty_session.commit()
    fetched_book = empty_session.query(Review).one()
    assert "Good" == fetched_book.review_text
