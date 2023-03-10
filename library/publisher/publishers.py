from flask import Blueprint, render_template, redirect, request, url_for

import library.adapters.repository as repo
import library.publisher.services as services

publishers_blueprint = Blueprint('publishers_bp', __name__)


@publishers_blueprint.route('/publishers', methods=['GET'])
def publishers():
    try:
        page_num = request.args.get("page")
        if page_num == None:
            page_num = 1
        else:
            page_num = int(page_num)
        pub = services.get_publishers(page_num, repo.repo_instance)
        if isinstance(pub, list):
            if pub[2] - 3 < 1:
                start_page = 1
            else:
                start_page = pub[2] - 3

            if pub[2] + 3 > pub[1]:
                end_page = pub[1]
            else:
                if pub[2] <= 3 and pub[2] + 5 <= pub[1]:
                    end_page = pub[2] + 5
                else:
                    end_page = pub[2] + 3
            return render_template('publishers/publishers.html', publishers=pub[0], end_page=end_page, page_num=pub[2],
                                   start_page=start_page, total_page=pub[1])
        else:
            raise ValueError
    except:
        return redirect(url_for('home_bp.home'))
