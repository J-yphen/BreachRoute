from flask_login import current_user, login_required, login_user, logout_user
from ..models import AppConfig, User
from werkzeug.security import check_password_hash
from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/admin')
@login_required
def admin():
    config = AppConfig.query.first()

    if not config.setup_complete:
        return redirect(url_for('onboarding.setup'))

    return render_template('breach/admin.html', username=current_user.username)

@bp.route('/login', methods=["GET", "POST"])
def login_handler():
    if request.method == "GET":
        return render_template('breach/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('main.login_handler'))
        login_user(user, remember=remember)
        return redirect(url_for('main.admin'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login_handler'))