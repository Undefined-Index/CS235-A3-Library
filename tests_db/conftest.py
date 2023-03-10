import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from library.adapters import database_repository
from library.adapters.orm import metadata, map_model_to_tables
import library.adapters.repository as repo
from library.adapters.jsondatareader import BooksJSONReader
from utils import get_project_root





TEST_DATA_PATH = get_project_root() / "tests" / "data"

path_to_books_file = str(get_project_root() / "tests" / "data"/'comic_books_excerpt.json')
path_to_authors_file = str(get_project_root() / "tests" / "data"/'book_authors_excerpt.json')

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///library.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repo_ins = BooksJSONReader(path_to_books_file, path_to_authors_file)
    repo_ins.read_json_files()
    repo.repo_instance.set_repo_book(repo_ins.dataset_of_books)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repo_ins = BooksJSONReader(path_to_books_file, path_to_authors_file)
    repo_ins.read_json_files()
    repo.repo_instance.set_repo_book(repo_ins.dataset_of_books)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)