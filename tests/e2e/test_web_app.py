import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/register',
        data={'username': 'testacc', 'password': 'eA86d4fA16Ef'}
    )
    assert response.headers['Location'] == 'http://localhost/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('test', 'wadaga8dffffffffffffffffffffffffffffffffffffff', b'The password can only and must contain 8 to 20 letters and numbers!'),
        ('cj', 'aa', b'The password can only and must contain 8 to 20 letters and numbers!'),
        ('test', '', b'The password can only and must contain 8 to 20 letters and numbers!'),
        ('', '6as4f894af51656', b'The username must and only contain more than 1 letter and number!'),
        ('testacc', 'eA86d4fA16Ef', b'Login'),
        ('testacc', 'eA86d4fA16Ef', b'The user already exists!'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    test_register(client)
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/login').status_code
    assert status_code == 200
    auth.register()
    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'testacc'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'username' not in session


def test_home_page(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Library System' in response.data


def test_login_required_to_comment(client):
    client.post(
        '/book?id=25742454',
        data={'rating': '5', 'review': 'test_text'}
    )
    response = client.get('/book?id=25742454')
    assert b'test_text' not in response.data


def test_comment(client, auth):
    # Login a user.
    auth.register()
    auth.login()

    # Check that we can retrieve the comment.
    client.post(
        '/book?id=13571772',
        data={'rating': '5', 'review': 'test text'}
    )
    response = client.get('/book?id=13571772')
    assert b'test text' in response.data

def test_comment_with_invalid_value(client, auth):
    # Login a user.
    auth.register()
    auth.login()

    # Check that we will redirect to home page
    response = client.post(
        '/book?id=13571772',
        data={'rating': '10', 'review': 'test text'}
    )
    assert response.status_code == 302

    response = client.post(
        '/book?id=13571772',
        data={'rating': '', 'review': 'test text'}
    )
    assert response.status_code == 302

    response = client.post(
        '/book?id=13571772',
        data={'rating': '', 'review': ''}
    )
    assert response.status_code == 302

def test_book_without_id(client):
    response = client.get('/book')
    # Check that we will redirect to home page
    assert response.status_code == 302

def test_book_with_wrong_id(client):
    response = client.get('/book?id=11111111')
    # Check that we will redirect to home page
    assert response.status_code == 302

def test_search(client):
    response = client.get('/books?Search=2016')
    assert response.status_code == 200
    assert b'War Stories, Volume 3' in response.data

def test_publishers(client):
    response = client.get('/publishers')
    assert response.status_code == 200
    assert b'Dargaud' in response.data

def test_authors(client):
    response = client.get('/authors')
    assert response.status_code == 200
    assert b'Lindsey Schussman' in response.data

def test_author(client):
    response = client.get('author?id=8551671')
    assert response.status_code == 200
    assert b'The Switchblade Mamma' in response.data
    response = client.get('author?id=aaaaaaaa')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('author?id=9999999999999')
    assert response.headers['Location'] == 'http://localhost/'

def test_publisher(client):
    response = client.get('publisher?name=DC%20Comics')
    assert response.status_code == 200
    assert b'Superman Archives, Vol. 2' in response.data
    response = client.get('publisher?name=abcdefghijklmn')
    assert response.headers['Location'] == 'http://localhost/'

def test_book(client):
    # Check that we can retrieve the book page.
    response = client.get('/book?id=25742454')
    assert response.status_code == 200
    assert b'Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American,' in response.data

def test_books(client):
    # Check that we can retrieve the books page.
    response = client.get('/books')
    assert response.status_code == 200
    assert b'The Switchblade Mamma' in response.data

def test_books_pager_with_invalid_value(client):
    response = client.get('/books?page=abcd')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/books?page=-1')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/books?page=99999')
    assert b'No Data Found' in response.data

def test_authors_pager_with_invalid_value(client):
    response = client.get('/authors?page=-1')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/authors?page=abcd')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/authors?page=999')
    assert b'No Data Found' in response.data

def test_publishers_pager_with_invalid_value(client):
    response = client.get('/publishers?page=-1')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/publishers?page=abcd')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/publishers?page=999')
    assert b'No Data Found' in response.data

def test_add_remove_search_in_want_to_read(client,auth):
    auth.register()
    auth.login()
    response = client.get('/add-want-to-read?ID=25742454')
    assert response.status_code == 302
    response = client.get('/want-to-read')
    assert b'The Switchblade Mamma' in response.data
    response = client.get('/want-to-read?Search=The Switch')
    assert b'The Switchblade Mamma' in response.data
    response = client.get('/add-want-to-read?ID=25742454')
    assert response.status_code == 302
    response = client.get('/want-to-read')
    assert b'No Data Found' in response.data

def test_add_invalid_value_to_want_to_read(client,auth):
    auth.register()
    auth.login()
    response = client.get('/add-want-to-read?ID=123456789')
    assert response.status_code == 302
    response = client.get('/add-want-to-read?ID=ABCDEFG')
    assert response.status_code == 302
    response = client.get('/want-to-read')
    assert b'No Data Found' in response.data

def test_want_to_read_pager_with_invalid_value(client,auth):
    auth.register()
    auth.login()
    response = client.get('/want-to-read?page=abcd')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/want-to-read?page=-1')
    assert response.headers['Location'] == 'http://localhost/'
    response = client.get('/want-to-read?page=99999')
    assert b'No Data Found' in response.data