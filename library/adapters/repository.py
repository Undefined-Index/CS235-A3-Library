import abc

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def set_repo_book(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get_repo_book(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_repo_user(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get_repo_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_repo_review(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get_repo_review(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_repo_want_to_read(self):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_repo_want_to_read(self):
        raise NotImplementedError
