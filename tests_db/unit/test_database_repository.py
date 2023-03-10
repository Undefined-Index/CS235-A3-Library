import pytest

from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import Review, User, Publisher, Book, Author


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    assert user in repo.get_repo_user()

def test_repository_can_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    getted_users = repo.get_repo_user()
    assert getted_users[0] == user and getted_users[0] is user

def test_repository_can_add_set_book_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "1")
    book2 = Book(2, "2")
    book3 = Book(3, "3")
    books = [book1, book2, book3]
    repo.set_repo_book(books)
    assert book1 in repo.get_repo_book()
    assert book2 in repo.get_repo_book()
    assert book3 in repo.get_repo_book()

def test_repository_can_get_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(1, "1")
    book2 = Book(2, "2")
    book3 = Book(3, "3")
    books = [book1, book2, book3]
    repo.set_repo_book(books)
    getted_book = repo.get_repo_book()
    assert book1 == getted_book[0]
    assert book2 == getted_book[1]
    assert book3 == getted_book[2]

def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(2675376, "Harry Potter")
    review_text = "  This book was very enjoyable.   "
    rating = 4
    review = Review(book, review_text, rating, 'testacc')
    repo.add_repo_review(review)
    assert repo.get_repo_review()[0] == review and repo.get_repo_review()[0] is review

def test_repository_can_get_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(2675376, "Harry Potter")
    review_text = "  This book was very enjoyable.   "
    rating = 4
    review = Review(book, review_text, rating, 'testacc')
    repo.add_repo_review(review)
    getted_review = repo.get_repo_review()
    assert getted_review[0] == review and getted_review[0] is review

def test_repository_can_add_remove_want_to_read(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(22222, "1")
    books = [book1]
    repo.set_repo_book(books)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    repo.add_repo_want_to_read(user.user_name,"22222")
    assert "22222" in user.want_to_read
    repo.remove_repo_want_to_read('dave', "22222")
    assert "22222" not in user.want_to_read

def test_repository_cant_add_want_to_read_invalid_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(22222, "1")
    books = [book1]
    repo.set_repo_book(books)
    with pytest.raises(TypeError):
        repo.add_repo_want_to_read(123,"22222")

def test_repository_cant_add_want_to_read_invalid_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    with pytest.raises(TypeError):
        repo.add_repo_want_to_read(user.user_name, 22222)

def test_repository_cant_remove_want_to_read_invalid_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(22222, "1")
    books = [book1]
    repo.set_repo_book(books)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    repo.add_repo_want_to_read(user.user_name,"22222")
    assert "22222" in user.want_to_read
    with pytest.raises(TypeError):
        repo.remove_repo_want_to_read(123, "22222")
    assert "22222" in user.want_to_read

def test_repository_cant_remove_want_to_read_invalid_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(22222, "1")
    books = [book1]
    repo.set_repo_book(books)
    user = User('dave', '123456789')
    repo.add_repo_user(user)
    repo.add_repo_want_to_read(user.user_name,"22222")
    assert "22222" in user.want_to_read
    with pytest.raises(TypeError):
        repo.remove_repo_want_to_read('dave', 22222)
    assert "22222" in user.want_to_read