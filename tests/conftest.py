import pytest
from pathlib import Path
from library import create_app
from library.adapters.jsondatareader import BooksJSONReader
from utils import get_project_root
from library.adapters import memory_repository
from library.adapters.memory_repository import MemoryRepository


TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    path_to_books_file = str(TEST_DATA_PATH/'comic_books_excerpt.json')
    path_to_authors_file = str(TEST_DATA_PATH/'book_authors_excerpt.json')
    repo_ins = BooksJSONReader(path_to_books_file, path_to_authors_file)
    repo_ins.read_json_files()
    repo = MemoryRepository()
    repo.set_repo_book(repo_ins.dataset_of_books)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, username='testacc', password='eA86d4fA16Ef'):
        return self.__client.post(
            '/register',
            data={'username': username, 'password': password}
        )


    def login(self, username='testacc', password='eA86d4fA16Ef'):
        return self.__client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
