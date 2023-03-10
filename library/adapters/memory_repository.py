from library.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__repo_instance_book = []
        self.__repo_instance_user = []
        self.__repo_instance_review = []

    def set_repo_book(self, value):
        if isinstance(value, list):
            self.__repo_instance_book = value
        else:
            raise TypeError

    def get_repo_book(self):
        return self.__repo_instance_book

    def add_repo_user(self, value):
        if isinstance(value, object):
            if (value not in self.__repo_instance_user):
                self.__repo_instance_user.append(value)
        else:
            raise TypeError

    def get_repo_user(self):
        return self.__repo_instance_user

    def add_repo_review(self, value):
        if isinstance(value, object):
            if (value not in self.__repo_instance_review):
                self.__repo_instance_review.append(value)
        else:
            raise TypeError

    def get_repo_review(self):
        return self.__repo_instance_review

    def add_repo_want_to_read(self, user, book):
        for i in self.__repo_instance_user:
            if i.user_name == user:
                i.add_book_to_want_to_read(book)

    def remove_repo_want_to_read(self, user, book):
        for i in self.__repo_instance_user:
            if i.user_name == user:
                i.remove_book_to_want_to_read(book)