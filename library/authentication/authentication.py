from flask import Blueprint, render_template, request, url_for, redirect, session

import library.adapters.repository as repo
import library.authentication.services as services

login_blueprint = Blueprint('login_bp', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # Determine request method
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            log = services.login_serv(username, password, repo.repo_instance)
            if log == True:
                session.clear()
                session['username'] = username.strip().lower()
                return redirect(url_for('home_bp.home'))
            return render_template('authentication/login.html', error=True)
        else:
            return render_template('authentication/login.html')

    except:
        return redirect(url_for('home_bp.home'))


register_blueprint = Blueprint('register_bp', __name__)


@register_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    try:
        # Determine request method
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            reg = services.register_serv(username, password, repo.repo_instance)
            if isinstance(reg, bool):
                return redirect(url_for('login_bp.login'))
            else:
                return render_template('authentication/register.html', error=reg)
        else:
            return render_template('authentication/register.html')

    except:
        return redirect(url_for('home_bp.home'))


logout_blueprint = Blueprint('logout_bp', __name__)


@logout_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))
