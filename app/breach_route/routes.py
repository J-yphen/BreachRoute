from ..models import AppConfig, User
from werkzeug.security import check_password_hash
from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/admin')
def admin():
    config = AppConfig.query.first()

    if not config.setup_complete:
        return redirect(url_for('onboarding.setup'))

    return render_template('breach/admin.html')

@bp.route('/login', methods=["GET", "POST"])
def login_handler():
    if request.method == "GET":
        return render_template('breach/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        # remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('main.login_handler'))

        return redirect(url_for('main.admin'))