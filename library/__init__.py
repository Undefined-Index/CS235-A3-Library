"""Initialize Flask app."""
from pathlib import Path

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import library.adapters.repository as repo
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters import memory_repository, database_repository
from library.adapters.orm import metadata, map_model_to_tables
from utils import get_project_root

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config.Config')
    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'
    csrf.init_app(app)  # register csrf
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        path_to_books_file = str(data_path / books_file_name)
        path_to_authors_file = str(data_path / authors_file_name)

    if app.config['REPOSITORY'] == 'memory':
        repo_ins = BooksJSONReader(path_to_books_file, path_to_authors_file)
        repo_ins.read_json_files()
        repo.repo_instance = memory_repository.MemoryRepository()
        repo.repo_instance.set_repo_book(repo_ins.dataset_of_books)


    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_model_to_tables()
            repo_ins = BooksJSONReader(path_to_books_file, path_to_authors_file)
            repo_ins.read_json_files()
            repo.repo_instance.set_repo_book(repo_ins.dataset_of_books)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .books import books
        app.register_blueprint(books.books_blueprint)

        from .books import book
        app.register_blueprint(book.book_blueprint)

        from .authors import author
        app.register_blueprint(author.author_blueprint)

        from .authors import authors
        app.register_blueprint(authors.authors_blueprint)

        from .publisher import publishers
        app.register_blueprint(publishers.publishers_blueprint)

        from .publisher import publisher
        app.register_blueprint(publisher.publisher_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.login_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.register_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.logout_blueprint)

        from .want_to_read import want_to_read
        app.register_blueprint(want_to_read.want_to_read_blueprint)

        from .want_to_read import want_to_read
        app.register_blueprint(want_to_read.add_want_to_read_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()
    return app
