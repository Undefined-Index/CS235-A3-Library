from flask import Blueprint, render_template, request, redirect, url_for

import library.adapters.repository as repo
import library.authors.services as services

author_blueprint = Blueprint('author_bp', __name__)


@author_blueprint.route('/author', methods=['GET'])
def author():
    try:
        ID = request.args.get("id")
        if ID == "":
            raise ValueError
        author = services.getauthor(ID, repo.repo_instance)
        if isinstance(author, list):
            return render_template('authors/author.html', authors=author[0], books=author[1])
        else:
            return redirect(url_for('home_bp.home'))
    except:
        return redirect(url_for('home_bp.home'))
