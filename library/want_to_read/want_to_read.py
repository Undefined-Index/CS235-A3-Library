from flask import Blueprint, redirect, request, render_template, url_for, session

import library.adapters.repository as repo
import library.want_to_read.services as services

want_to_read_blueprint = Blueprint('want_to_read_bp', __name__)


@want_to_read_blueprint.route('/want-to-read', methods=['GET'])
def want_to_read():
    try:
        if session.get('username') != None:
            search_word = request.args.get("Search")
            page_num = request.args.get("page")
            if page_num == None:
                page_num = 1
            else:
                page_num = int(page_num)
            if search_word != None and len(search_word) > 0:
                wtr_list = services.search_want_to_read(session.get('username'), page_num, search_word,
                                                        repo.repo_instance)
                if isinstance(wtr_list, list):
                    if wtr_list[2] - 3 < 1:
                        start_page = 1
                    else:
                        start_page = wtr_list[2] - 3

                    if wtr_list[2] + 3 > wtr_list[1]:
                        end_page = wtr_list[1]
                    else:
                        if wtr_list[2] <= 3 and wtr_list[2] + 5 <= wtr_list[1]:
                            end_page = wtr_list[2] + 5
                        else:
                            end_page = wtr_list[2] + 3
                    return render_template('want_to_read/book_list.html', books=wtr_list[0],
                                           end_page=end_page, page_num=wtr_list[2], start_page=start_page,
                                           total_page=wtr_list[1])
                else:
                    raise ValueError
            else:
                wtr_list = services.get_want_to_read(session.get('username'), page_num, repo.repo_instance)
                if isinstance(wtr_list, list):
                    if wtr_list[2] - 3 < 1:
                        start_page = 1
                    else:
                        start_page = wtr_list[2] - 3

                    if wtr_list[2] + 3 > wtr_list[1]:
                        end_page = wtr_list[1]
                    else:
                        if wtr_list[2] <= 3 and wtr_list[2] + 5 <= wtr_list[1]:
                            end_page = wtr_list[2] + 5
                        else:
                            end_page = wtr_list[2] + 3
                    return render_template('want_to_read/book_list.html', books=wtr_list[0],
                                           end_page=end_page, page_num=wtr_list[2], start_page=start_page,
                                           total_page=wtr_list[1])
                else:
                    raise ValueError
        raise ValueError
    except:
        return redirect(url_for('home_bp.home'))


add_want_to_read_blueprint = Blueprint('add_want_to_read_bp', __name__)


@add_want_to_read_blueprint.route('/add-want-to-read', methods=['GET'])
def add_want_to_read():
    try:
        if session.get('username') == None:
            return redirect(url_for('login_bp.login'))
        ID = request.args.get("ID")
        if ID == None:
            raise ValueError
        add_wtr = services.add_want_to_read(ID, session.get('username'), repo.repo_instance)
        if add_wtr == 0:
            return redirect("book?id=" + ID)
        elif add_wtr == 1:
            raise ValueError
        else:
            return redirect(url_for('login_bp.login'))
    except:
        return redirect(url_for('home_bp.home'))
