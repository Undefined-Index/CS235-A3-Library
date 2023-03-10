import math

from library.adapters.repository import AbstractRepository
from library.to_dict.to_dict import book_to_dict


def get_want_to_read(username: str, page_num: int, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    user_list = repo.get_repo_user()
    for z in user_list:
        if username.strip().lower() == z.user_name:
            books = []
            for i in z.want_to_read.split(","):
                for a in books_list:
                    if i == str(a.book_id):
                        books.append(book_to_dict(a))

            start_page = (int(page_num) - 1) * 10
            end_page = start_page + 10
            num_books = len(books)
            total_page = math.ceil(num_books / 10)
            if page_num < 0:
                return False
            return [books[start_page:end_page], total_page, page_num]


def search_want_to_read(username: str, page_num: int, search_word: str, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    user_list = repo.get_repo_user()
    for z in user_list:
        if username.strip().lower() == z.user_name:
            books = []
            for i in z.want_to_read.split(","):
                for a in books_list:
                    if i == str(a.book_id):
                        books.append(a)
            start_page = (int(page_num) - 1) * 10
            end_page = start_page + 10
            search_word = search_word.lower()
            search_data = []
            for i in books:
                if search_word in i.title.lower() or search_word in i.publisher.name.lower() or search_word == str(
                        i.release_year):
                    search_data.append(book_to_dict(i))
                else:
                    for x in i.authors:
                        if search_word in x.full_name.lower():
                            search_data.append(book_to_dict(i))
            num_books = len(search_data)
            total_page = math.ceil(num_books / 10)
            if page_num < 0:
                return False
            return [search_data[start_page:end_page], total_page, page_num]


def add_want_to_read(ID: int, username: str, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    user_list = repo.get_repo_user()
    book_exist = False
    for i in books_list:
        if i.book_id == int(ID):
            book_exist = True
            break
    if book_exist == False:
        return 1

    if username != None:
        for z in user_list:
            if username == z.user_name:
                if str(ID) in z.want_to_read.split(","):
                    repo.remove_repo_want_to_read(z.user_name, str(ID))
                else:
                    repo.add_repo_want_to_read(z.user_name,str(ID))
                return 0
    return 2
