from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_author', 'books', 'publishers', 'reviews', 'users']

def test_database_populate_authors(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['authors']])
        result = connection.execute(select_statement)

        authors_names = []
        for row in result:
            authors_names.append(row['full_name'])

        assert "Garth Ennis" in authors_names #first one
        assert "Jason Delgado" in authors_names #last one

def test_database_populate_select_all_books(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['books']])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['book_id'], row['title']))

        assert len(all_books) == 20
        assert (25742454, 'The Switchblade Mamma') in all_books

def test_database_populate_publishers(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['publishers']])
        result = connection.execute(select_statement)

        publishers_names = []
        for row in result:
            publishers_names.append(row['name'])

        assert "Go! Comi" in publishers_names
        assert "Dargaud" in publishers_names
