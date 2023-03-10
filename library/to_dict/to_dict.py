from library.domain.model import Review, Publisher, Book, Author
import urllib.parse


def book_to_dict(book: Book):
    author_list = []
    for author in book.authors:
        author_list.append(author_to_dict(author))
    book_dict = {
        'book_id': book.book_id,
        'book_title': book.title,
        'description': book.description,
        'publisher': book.publisher.name,
        'publisher_url': urllib.parse.quote_plus(book.publisher.name),
        'authors': author_list,
        'release_year': book.release_year,
        'ebook': book.ebook,
        'num_pages': book.num_pages
    }
    return book_dict


def review_to_dict(review: Review):
    review_dict = {
        'book': book_to_dict(review.book),
        'review_text': review.review_text,
        'rating': review.rating,
        'user': review.user,
        'timestamp': review.timestamp
    }
    return review_dict


def author_to_dict(author: Author):
    author_dict = {
        'author_id': author.unique_id,
        'author_full_name': author.full_name,
    }
    return author_dict
