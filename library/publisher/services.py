import math
import urllib.parse
from library.adapters.repository import AbstractRepository
from library.to_dict.to_dict import book_to_dict


def get_publisher(name: str, repo: AbstractRepository):
    if name == "":
        return False
    books = []
    for i in repo.get_repo_book():
        if i.publisher.name == name:
            books.append(book_to_dict(i))
    return books


def get_publishers(page_num: None, repo: AbstractRepository):
    if isinstance(page_num, int):
        if page_num < 0:
            return False
    else:
        return False
    publishers_list = []
    for i in repo.get_repo_book():
        if i.publisher.name != "N/A" and i.publisher.name not in publishers_list:
            publishers_list.append([i.publisher.name,urllib.parse.quote_plus(i.publisher.name)])
    start_page = (int(page_num) - 1) * 50
    end_page = start_page + 50
    num_authors = len(publishers_list)
    total_page = math.ceil(num_authors / 50)
    return [publishers_list[start_page:end_page], total_page, page_num]
