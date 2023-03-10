from flask import Blueprint, render_template, request, redirect, url_for

import library.adapters.repository as repo
import library.books.services as services

books_blueprint = Blueprint('books_bp', __name__)


@books_blueprint.route('/books', methods=['GET'])
def books():
    try:
        search_word = request.args.get("Search")
        page_num = request.args.get("page")

        if search_word != None and len(search_word) > 0:
            books = services.search_book(page_num, search_word, repo.repo_instance)
            if isinstance(books, list):
                if books[2] - 3 < 1:
                    start_page = 1
                else:
                    start_page = books[2] - 3

                if books[2] + 3 > books[1]:
                    end_page = books[1]
                else:
                    if books[2] <= 3 and books[2] + 5 <= books[1]:
                        end_page = books[2] + 5
                    else:
                        end_page = books[2] + 3
                return render_template('books/books.html', books=books[0], end_page=end_page,
                                       page_num=books[2], search_word=search_word, start_page=start_page,
                                       total_page=books[1])
            else:
                raise ValueError
        else:
            books = services.get_books(page_num, repo.repo_instance)
            if isinstance(books, list):
                if books[2] - 3 < 1:
                    start_page = 1
                else:
                    start_page = books[2] - 3

                if books[2] + 3 > books[1]:
                    end_page = books[1]
                else:
                    if books[2] <= 3 and books[2] + 5 <= books[1]:
                        end_page = books[2] + 5
                    else:
                        end_page = books[2] + 3
                return render_template('books/books.html', books=books[0], end_page=end_page,
                                       page_num=books[2], start_page=start_page, total_page=books[1])
            else:
                raise ValueError
    except:
        return redirect(url_for('home_bp.home'))
