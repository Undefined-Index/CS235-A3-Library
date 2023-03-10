import pytest
from library.authentication import services as auth_services
from library.authors import services as authors_services
from library.books import services as books_services
from library.publisher import services as publisher_services
from library.want_to_read import services as want_to_read_services
#auth_services tests:
def test_register_serv_all_valid(in_memory_repo):
    username = '123'
    password = '12341234'
    result = auth_services.register_serv(username, password, in_memory_repo)
    assert result == True
    user_dict = auth_services.get_user_dict(username, in_memory_repo)
    assert user_dict['user_name'] == '123'
    assert user_dict['password'].startswith('ed2b1f468')

def test_register_serv_repeat_name(in_memory_repo):
    username = '123'
    password = '12341234'
    result = auth_services.register_serv(username, password, in_memory_repo)
    assert result == True
    user_dict = auth_services.get_user_dict(username, in_memory_repo)
    assert user_dict['user_name'] == '123'
    assert user_dict['password'].startswith('ed2b1f468')

    result = auth_services.register_serv(username, password, in_memory_repo)
    assert result == 2

def test_register_serv_invalid_user_name(in_memory_repo):
    username = ''
    password = '12341234'
    result = auth_services.register_serv(username, password, in_memory_repo)
    assert result == 3

def test_register_serv_invalid_password(in_memory_repo):
    username = '123'
    password = '123'
    result = auth_services.register_serv(username, password, in_memory_repo)
    assert result == 1

def test_login_serv_valid(in_memory_repo):
    test_register_serv_all_valid(in_memory_repo)
    result = auth_services.login_serv('123', '12341234', in_memory_repo)
    assert result == True

def test_login_serv_non_regiested_user_cant_login(in_memory_repo):
    result = auth_services.login_serv('12', '123123', in_memory_repo)
    assert result == False


#authors_services tests:
def test_getauthor_valid_id(in_memory_repo):
    id = 3188368
    result = authors_services.getauthor(id, in_memory_repo)
    assert result[0]['author_id'] == 3188368
    assert result[0]['author_full_name'] == "Tomas Aira"
    assert result[1][0]['book_title'] == "War Stories, Volume 3"
    assert result[1][1]['book_title'] == "War Stories, Volume 4"
    assert len(result[1]) == 2

def test_getauthor_invalid_id(in_memory_repo):
    id = 318836
    result = authors_services.getauthor(id, in_memory_repo)
    assert result == False

def test_getauthors_valid_page(in_memory_repo):
    page = "1"
    result = authors_services.getauthors(page, in_memory_repo)
    assert len(result) == 3
    assert len(result[0]) == 31
    assert result[1] == 1
    assert result[2] == 1

    expecte_authors_name = ['Lindsey Schussman', 'Florence Dupre la Tour', 'Ed Brubaker', 'Jason Delgado',
                            'Chris Martin', 'Jerry Siegel', 'Joe Shuster', 'Yuu Asami', 'Garth Ennis',
                            'Tomas Aira', 'Keith Burns', 'Matt Martin', 'Mike Wolfer', 'Simon Spurrier',
                            'Fernando Heinz', 'Rafael Ortiz', 'DigiKore Studios', 'Jaymes Reed', 'Jeon Geuk-Jin',
                            'Scott Beatty', 'Daniel Indro', 'Naoki Urasawa', 'Rich Tommaso', 'Maki Minami',
                            'Takashi Murakami', 'Cun Shang Chong', 'Asma', 'Dan Slott', 'Andrea DiVito',
                            'Kieron Dwyer', 'Katsura Hoshino']
    for i in range(len(result[0])):
        assert result[0][i]['author_full_name'].replace(' ', '') == expecte_authors_name[i].replace(' ','')


def test_getauthors_invalid_page_value_error(in_memory_repo):
    page = "a"
    with pytest.raises(ValueError):
        authors_services.getauthors(page, in_memory_repo)

def test_getauthors_invalid_page_out_of_range1(in_memory_repo):
    page = "-1"
    result = authors_services.getauthors(page, in_memory_repo)
    assert result == False

def test_getauthors_invalid_page_out_of_range2(in_memory_repo):
    page = "-10"
    result = authors_services.getauthors(page, in_memory_repo)
    assert result == False

#books_services tests:
def test_can_get_non_wanna_read_book_not_logged_in(in_memory_repo):
    ID = "25742454"
    result = books_services.get_book(ID, None, in_memory_repo)
    assert result[0]['book_id'] == 25742454
    assert result[0]['book_title'] == 'The Switchblade Mamma'
    assert result[0]['publisher'] == 'N/A'
    assert result[0]['release_year'] == None

    assert result[1] == False

def test_can_get_wanna_read_book_logged_in(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    want_to_read_services.add_want_to_read(ID, username, in_memory_repo)

    result = books_services.get_book(ID, username, in_memory_repo)

    assert result[0]['book_id'] == 25742454
    assert result[0]['book_title'] == 'The Switchblade Mamma'
    assert result[0]['publisher'] == 'N/A'
    assert result[0]['release_year'] == None

    assert result[1] == True

def test_cant_get_wanna_read_book_not_logged_in(in_memory_repo):
    ID = "25742454"
    want_to_read_services.add_want_to_read(ID, None, in_memory_repo)
    result = books_services.get_book(ID, None, in_memory_repo)
    assert result[1] == False

def test_can_get_non_wanna_read_book_logged_in(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    result = books_services.get_book(ID, username, in_memory_repo)

    assert result[0]['book_id'] == 25742454
    assert result[0]['book_title'] == 'The Switchblade Mamma'
    assert result[0]['publisher'] == 'N/A'
    assert result[0]['release_year'] == None
    assert result[1] == False

def test_cant_get_book_with_invalid_ID1(in_memory_repo):
    ID = "123"
    result = books_services.get_book(ID, None, in_memory_repo)
    assert result == False

def test_cant_get_book_with_invalid_ID2(in_memory_repo):
    ID = "abc"
    with pytest.raises(ValueError):
        books_services.get_book(ID, None, in_memory_repo)

def test_logged_in_user_can_add_review(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    result = books_services.add_review(ID, username, "5", "nice book", in_memory_repo)
    review = books_services.get_review(ID, in_memory_repo)

    assert result == True
    assert len(review) == 1
    assert review[0]['book']['book_id'] == 25742454
    assert review[0]['rating'] == 5
    assert review[0]['review_text'] == 'nice book'
    assert review[0]['user'] == '123'

def test_cant_add_review_not_logged_in(in_memory_repo):
    ID = "25742454"
    result = books_services.add_review(ID, None, "5", "nice book", in_memory_repo)
    assert result == False

def test_cant_add_review_invalid_rating(in_memory_repo):
    username = '123'
    password = '123123'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    result = books_services.add_review(ID, username, "6", "nice book", in_memory_repo)
    assert result == False

def test_cant_add_review_invalid_review1(in_memory_repo):
    username = '123'
    password = '123123'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    result = books_services.add_review(ID, username, "6", '', in_memory_repo)
    assert result == False

def test_cant_add_review_invalid_review2(in_memory_repo):
    username = '123'
    password = '123123'
    auth_services.register_serv(username, password, in_memory_repo)

    ID = "25742454"
    result = books_services.add_review(ID, username, "6", 123, in_memory_repo)
    assert result == False

#assume id is valid, invalid id will be handled by the view layer
def test_can_get_review(in_memory_repo):
    ID = "25742454"
    review = books_services.get_review(ID, in_memory_repo)
    assert review == []

def test_can_get_books_all_valid(in_memory_repo):
    result = books_services.get_books(1, in_memory_repo)
    assert len(result[0]) == 10
    expect_title = ['The Switchblade Mamma', 'Cruelle',
                    'Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)',
                    'Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC',
                    'Superman Archives, Vol. 2', 'A.I. Revolution, Vol. 1', 'War Stories, Volume 3', 'Crossed, Volume 15',
                    'Crossed + One Hundred, Volume 2 (Crossed +100 #2)', 'War Stories, Volume 4']
    for i in range(len(result[0])):
        assert result[0][i][ 'book_title'] == expect_title[i]

def test_cant_get_books_invalid_page1(in_memory_repo):
    result = books_services.get_books(-1, in_memory_repo)
    assert result == False

def test_cant_get_books_invalid_page2(in_memory_repo):
    with pytest.raises(ValueError):
        books_services.get_books("a", in_memory_repo)

def test_can_search_book_alL_valid(in_memory_repo):
    search_word = 'Cruelle'
    result = books_services.search_book(1, search_word, in_memory_repo)
    assert result[1] == 1
    assert result[2] == 1
    assert len(result[0]) == 1
    assert result[0][0]['book_id'] == 30128855
    assert result[0][0]['book_title'] == 'Cruelle'

def test_cant_search_book_invalid_page1(in_memory_repo):
    search_word = 'Cruelle'
    result = books_services.search_book(-1, search_word, in_memory_repo)
    assert result == False

def test_cant_search_book_invalid_page2(in_memory_repo):
    search_word = 'Cruelle'
    with pytest.raises(ValueError):
        books_services.search_book("a", search_word, in_memory_repo)

def test_cant_search_book_invalid_search_word(in_memory_repo):
    search_word = None
    result = books_services.search_book(1, search_word, in_memory_repo)
    assert result == False


#publisher_services tests:
def test_can_get_publisher_all_valid(in_memory_repo):
    publisher_name = 'Dargaud'
    book = publisher_services.get_publisher(publisher_name, in_memory_repo)
    assert len(book) == 1
    assert book[0]['book_title'] == 'Cruelle'
    assert book[0]['book_id'] == 30128855

def test_cant_get_publisher_invalid_publisher_name(in_memory_repo):
    publisher_name = ''
    result = publisher_services.get_publisher(publisher_name, in_memory_repo)
    assert result == False

def test_can_get_publishers_all_valid(in_memory_repo):
    result = publisher_services.get_publishers(1, in_memory_repo)
    assert len(result) == 3
    assert len(result[0]) > 0

def test_cant_get_publishers_invalid_page_num1(in_memory_repo):
    result = publisher_services.get_publishers(-1, in_memory_repo)
    assert result == False

def test_cant_get_publishers_invalid_page_num2(in_memory_repo):
    assert publisher_services.get_publishers("a", in_memory_repo) == False

#want_to_read_services tests:

#assuming username is valid, since user can only see Want to read button once they logged in
def test_can_get_want_to_read_all_valid(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    want_to_read_services.add_want_to_read(30128855, username, in_memory_repo)
    result = want_to_read_services.get_want_to_read(username, 1, in_memory_repo)
    assert len(result) == 3
    assert len(result[0]) == 1
    assert result[0][0]['book_id'] == 30128855
    assert result[0][0]['book_title'] == 'Cruelle'

def test_can_get_want_to_read_if_not_add_any_books(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    result = want_to_read_services.get_want_to_read(username, 1, in_memory_repo)
    assert len(result) == 3
    assert result[0] == []
    assert result[1] == 0
    assert result[2] == 1

def test_cant_get_want_to_read_if_page_out_of_range(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    result = want_to_read_services.get_want_to_read(username, -1, in_memory_repo)
    assert result == False

def test_cant_get_want_to_read_if_not_logged_in(in_memory_repo):
    result = want_to_read_services.get_want_to_read(None, 1, in_memory_repo)
    assert result == None

def test_can_search_want_to_read_all_valid(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    want_to_read_services.add_want_to_read(30128855, username, in_memory_repo)
    result = want_to_read_services.search_want_to_read(username, 1, 'Cruelle', in_memory_repo)
    assert len(result) == 3
    assert len(result[0]) == 1
    assert result[0][0]['book_id'] == 30128855
    assert result[0][0]['book_title'] == 'Cruelle'

def test_cant_search_want_to_read_if_page_out_of_range(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    result = want_to_read_services.search_want_to_read(username, -1, 'Cruelle', in_memory_repo)
    assert result == False

def test_cant_search_want_to_read_if_not_logged_in(in_memory_repo):
    result = want_to_read_services.search_want_to_read(None, 1, 'Cruelle', in_memory_repo)
    assert result == None

def test_can_add_want_to_read_all_valid(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    result = want_to_read_services.add_want_to_read(30128855, username, in_memory_repo)
    assert result == 0

def test_cant_add_want_to_read_if_book_non_exist(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)

    result = want_to_read_services.add_want_to_read(3012885, username, in_memory_repo)
    assert result == 1

def test_cant_add_want_to_read_if_not_logged_in(in_memory_repo):
    result = want_to_read_services.add_want_to_read(30128855, None, in_memory_repo)
    assert result == 2

def test_cant_add_want_to_read_invalid_id(in_memory_repo):
    username = '123'
    password = '12341234'
    auth_services.register_serv(username, password, in_memory_repo)
    with pytest.raises(ValueError):
        want_to_read_services.add_want_to_read("a", username, in_memory_repo)

