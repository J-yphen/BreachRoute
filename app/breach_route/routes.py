from ..models import AppConfig, User
from werkzeug.utils import secure_filename
from app.utils.route_utils import fetch_all_route, register_route, render_route
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/admin')
@login_required
def admin():
    config = AppConfig.query.first()

    if not config.setup_complete:
        return redirect(url_for('onboarding.setup'))

    return render_template('breach/admin.html', username=current_user.username, route_list=fetch_all_route())

@bp.route('/login', methods=["GET", "POST"])
def login_handler():
    config = AppConfig.query.first()

    if not config.setup_complete:
        return redirect(url_for('onboarding.setup'))
    
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

@bp.route('/add_route', methods=['POST'])
@login_required
def add_route():
    url_path = request.form.get('url_path')
    filename = secure_filename(request.form.get('filename'))
    payload = request.form.get('payload')

    if not filename:
        flash("Filename is required")
        # return jsonify({"error": "Filename is required"}), 400
        return redirect(url_for('main.admin'))
    
    if request.files.get('file-payload').filename != "":
        payload_file = request.files['file-payload']
        res = register_route(url_path=url_path, filename=filename, payload=payload_file, isFile=True)
        flash(res)
        return redirect(url_for('main.admin'))

    elif payload:
        res = register_route(url_path=url_path, filename=filename, payload=payload, isFile=False)
        flash(res)
        return redirect(url_for('main.admin'))
    else:
        flash("Payload is required")
        # return jsonify({"error": "Payload is required"}), 400
        return redirect(url_for('main.admin'))
    
@bp.route('/update_route', methods=['POST'])
@login_required
def update_route():
    return "Test"

@bp.route('/<path:dynamic_path>')
def dynamic_handler(dynamic_path):
    return render_route(dynamic_path)