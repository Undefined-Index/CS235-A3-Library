from flask import Blueprint, render_template, request, redirect, url_for

import library.adapters.repository as repo
import library.publisher.services as services

publisher_blueprint = Blueprint('publisher_bp', __name__)


@publisher_blueprint.route('/publisher', methods=['GET'])
def publisher():
    try:
        name = request.args.get("name")
        if name == None:
            raise ValueError
        books = services.get_publisher(name, repo.repo_instance)
        if isinstance(books, list):
            if len(books) > 0:
                return render_template('publishers/publisher.html', books=books, name=name)
            raise ValueError
        else:
            raise ValueError
    except:
        return redirect(url_for('home_bp.home'))
