from flask import Blueprint, render_template, redirect, request, url_for

import library.adapters.repository as repo
import library.authors.services as services

authors_blueprint = Blueprint('authors_bp', __name__)


@authors_blueprint.route('/authors', methods=['GET'])
def authors():
    try:
        page_num = request.args.get("page")
        authors_ret = services.getauthors(page_num, repo.repo_instance)
        if isinstance(authors_ret, list):
            if authors_ret[2] - 3 < 1:
                start_page = 1
            else:
                start_page = authors_ret[2] - 3

            if authors_ret[2] + 3 > authors_ret[1]:
                end_page = authors_ret[1]
            else:
                if authors_ret[2] <= 3 and authors_ret[2] + 5 <= authors_ret[1]:
                    end_page = authors_ret[2] + 5
                else:
                    end_page = authors_ret[2] + 3
            return render_template('authors/authors.html', authors=authors_ret[0], end_page=end_page,
                                   page_num=authors_ret[2], start_page=start_page, total_page=authors_ret[1])
        else:
            raise ValueError
    except:
        return redirect(url_for('home_bp.home'))
