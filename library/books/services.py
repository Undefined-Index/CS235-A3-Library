import math

from library.adapters.repository import AbstractRepository
from library.domain.model import Review
from library.to_dict.to_dict import book_to_dict, review_to_dict


def get_book(ID: int, username: None, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    user_list = repo.get_repo_user()
    this_book = None
    wanna_read = False
    for i in books_list:
        if i.book_id == int(ID):
            this_book = i
    if this_book == None:
        return False

    if username != None:
        for z in user_list:
            if username == z.user_name:
                if ID in z.want_to_read.split(","):
                    wanna_read = True
    return [book_to_dict(this_book), wanna_read]


def get_review(ID: int, repo: AbstractRepository):
    this_book = None
    review_list = []
    books_list = repo.get_repo_book()
    for i in books_list:
        if i.book_id == int(ID):
            this_book = i

    for x in repo.get_repo_review():
        if this_book == x.book:
            review_list.append(review_to_dict(x))
    return review_list


def add_review(ID: int, username: str, rating: str, review: str, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    for i in books_list:
        if i.book_id == int(ID):
            this_book = i

    for z in repo.get_repo_user():
        if username == z.user_name:
            if int(rating) > 0 and int(rating) < 6 and isinstance(review, str) and len(review) > 0:
                repo.add_repo_review(Review(this_book, review, int(rating), z.user_name))
                return True
    return False


def get_books(page_num: None, repo: AbstractRepository):
    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)
    start_page = (int(page_num) - 1) * 10
    end_page = start_page + 10
    books_data = repo.get_repo_book()
    num_books = len(books_data)
    total_page = math.ceil(num_books / 10)
    if page_num < 0:
        return False
    books_data = books_data[start_page:end_page]
    for i in range(len(books_data)):
        books_data[i] = book_to_dict(books_data[i])
    return [books_data, total_page, page_num]


def search_book(page_num: None, search_word: None, repo: AbstractRepository):
    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)
    if page_num < 0:
        return False
    start_page = (int(page_num) - 1) * 10
    end_page = start_page + 10
    books_data = repo.get_repo_book()
    if search_word != None:
        search_word = search_word.lower()
        search_data = []
        for i in books_data:
            if search_word in i.title.lower() or search_word in i.publisher.name.lower() or search_word == str(
                    i.release_year):
                search_data.append(i)
            else:
                for x in i.authors:
                    if search_word in x.full_name.lower():
                        search_data.append(i)
        num_books = len(search_data)
        total_page = math.ceil(num_books / 10)
        search_data = search_data[start_page:end_page]
        for i in range(len(search_data)):
            search_data[i] = book_to_dict(search_data[i])
        return [search_data, total_page, page_num]
    else:
        return False
