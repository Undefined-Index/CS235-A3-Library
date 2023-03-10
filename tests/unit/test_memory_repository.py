from datetime import date, datetime
from typing import List

import pytest

from library.domain.model import Review, User, Publisher, Book, Author


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_repo_user(user)
    assert user in in_memory_repo.get_repo_user()

def test_repository_can_add_set_book_list(in_memory_repo):
    book1 = Book(1, "1")
    book2 = Book(2, "2")
    book3 = Book(3, "3")
    books = [book1,book2,book3]
    in_memory_repo.set_repo_book(books)
    assert books == in_memory_repo.get_repo_book()
    
def test_repository_can_add_a_review(in_memory_repo):
    book = Book(2675376, "Harry Potter")
    review_text = "  This book was very enjoyable.   "
    rating = 4
    review = Review(book, review_text, rating,'testacc')
    in_memory_repo.add_repo_review(review)
    assert in_memory_repo.get_repo_review()[0] == review
    
def test_repository_add_remove_want_to_read(in_memory_repo):
    book1 = Book(22222, "1")
    books = [book1]
    in_memory_repo.set_repo_book(books)
    user = User('dave', '123456789')
    in_memory_repo.add_repo_user(user)
    in_memory_repo.add_repo_want_to_read(user.user_name,"22222")
    assert "22222" in user.want_to_read