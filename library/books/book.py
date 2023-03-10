from flask import Blueprint, render_template, request, redirect, url_for, session

import library.adapters.repository as repo
import library.books.services as services

book_blueprint = Blueprint('book_bp', __name__)


@book_blueprint.route('/book', methods=['GET', 'POST'])
def book():
    try:
        ID = request.args.get("id")
        if ID == None:
            raise ValueError
        book_list = services.get_book(ID, session.get('username'), repo.repo_instance)
        if isinstance(book_list, list):
            pass
        else:
            raise ValueError
        review_list = services.get_review(ID, repo.repo_instance)

        # Add review
        if request.method == 'POST':
            if session.get('username') != None:
                rating = request.form.get("rating")
                review = request.form.get("review")
                addreivew = services.add_review(ID, session.get('username'), rating, review, repo.repo_instance)
                if addreivew == True:
                    return redirect("book?id=" + ID)
                else:
                    raise ValueError
        return render_template('books/book.html', book=book_list[0], reviews=review_list, wanna_read=book_list[1])

    except:
        return redirect(url_for('home_bp.home'))
