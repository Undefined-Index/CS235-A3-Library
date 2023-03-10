from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import User, Book, Review, Publisher, Author
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def set_repo_book(self, value):
        if isinstance(value, list):
            for i in value:
                with self._session_cm as scm:
                    scm.session.merge(i)
                    scm.commit()
        else:
            raise TypeError

    def get_repo_book(self):
        books = self._session_cm.session.query(Book).all()
        return books

    def add_repo_user(self, value):
        if isinstance(value, object):
            user_obj = self._session_cm.session.query(User).filter(User == value)
            if user_obj.count() == 0:
                with self._session_cm as scm:
                    scm.session.add(value)
                    scm.commit()
        else:
            raise TypeError

    def get_repo_user(self):
        user = self._session_cm.session.query(User).all()
        return user

    def add_repo_review(self, value):
        if isinstance(value, object):
            review_obj = self._session_cm.session.query(Review).filter(Review == value)
            if review_obj.count() == 0:
                with self._session_cm as scm:
                    scm.session.add(value)
                    scm.commit()
        else:
            raise TypeError

    def get_repo_review(self):
        review = self._session_cm.session.query(Review).all()
        return review

    def add_repo_want_to_read(self, user, book):
        if isinstance(user, str) and isinstance(book, str):
            user_obj = self._session_cm.session.query(User).get(user)
            list = user_obj.want_to_read
            list = list + "," + book + ","
            user_obj._User__want_to_read = list
            with self._session_cm as scm:
                scm.commit()
        else:
            raise TypeError

    def remove_repo_want_to_read(self, user, book):
        if isinstance(user, str) and isinstance(book, str):
            user_obj = self._session_cm.session.query(User).get(user)
            list = user_obj.want_to_read
            if book in list:
                user_obj._User__want_to_read = list.replace(","+book+",","")
                with self._session_cm as scm:
                    scm.commit()
        else:
            raise TypeError