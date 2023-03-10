import math

from library.adapters.repository import AbstractRepository
from library.to_dict.to_dict import book_to_dict, author_to_dict


def getauthor(ID: int, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    authors_list = []
    for a in books_list:
        for x in a.authors:
            authors_list.append(x)
    books = []
    for i in authors_list:
        if i.unique_id == int(ID):
            for x in books_list:
                if i in x.authors:
                    books.append(book_to_dict(x))
            return [author_to_dict(i), books]
    return False


def getauthors(page_num: int, repo: AbstractRepository):
    books_list = repo.get_repo_book()
    authors_list = []
    for a in books_list:
        for x in a.authors:
            if x not in authors_list:
                authors_list.append(x)
    if page_num == None:
        page_num = 1
    else:
        page_num = int(page_num)
    start_page = (int(page_num) - 1) * 50
    end_page = start_page + 50
    num_authors = len(authors_list)
    total_page = math.ceil(num_authors / 50)
    if page_num < 0:
        return False
    authors_list = authors_list[start_page:end_page]
    for i in range(len(authors_list)):
        authors_list[i] = author_to_dict(authors_list[i])
    return [authors_list, total_page, page_num]
