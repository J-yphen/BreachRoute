from ..models import AppConfig, User
from werkzeug.utils import secure_filename
from app.utils.route_utils import fetch_all_route, fetch_route_payload, modify_route, modify_route_visibility, register_route, remove_route, render_route, search_route
from werkzeug.security import check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

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
            flash("Please check your login details and try again.", "error")
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
        flash("Filename is required", "info")
        # return jsonify({"error": "Filename is required"}), 400
        return redirect(url_for('main.admin'))
    
    if request.files.get('file-payload').filename != "":
        payload_file = request.files['file-payload']
        res, catgry = register_route(url_path=url_path, filename=filename, payload=payload_file, isFile=True)
        flash(res, catgry)
        return redirect(url_for('main.admin'))
    elif payload:
        res, catgry = register_route(url_path=url_path, filename=filename, payload=payload, isFile=False)
        flash(res, catgry)
        return redirect(url_for('main.admin'))
    else:
        flash("Payload is required", "info")
        # return jsonify({"error": "Payload is required"}), 400
        return redirect(url_for('main.admin'))
    
@bp.route('/update_route', methods=['POST'])
@login_required
def update_route():
    url_path = request.form.get('url_path')
    filename = secure_filename(request.form.get('filename'))
    payload = request.form.get('payload')
    old_url_path_id = request.form.get('update-path')

    if not filename:
        flash("Filename is required", "info")
        return redirect(url_for('main.admin'))
    
    if request.files.get('file-payload').filename != "":
        payload_file = request.files['file-payload']
        res, catgry = modify_route(old_url_path_id=old_url_path_id, new_url_path=url_path, new_filename=filename, payload=payload_file, isFile=True)
        flash(res, catgry)
        return redirect(url_for('main.admin'))

    elif payload:
        res, catgry = modify_route(old_url_path_id=old_url_path_id, new_url_path=url_path, new_filename=filename, payload=payload, isFile=False)
        flash(res, catgry)
        return redirect(url_for('main.admin'))
    else:
        flash("Payload is required", "info")
        return redirect(url_for('main.admin'))

@bp.route('/update_route_visibility/<path:url_path>', methods=['GET'])
@login_required
def update_route_visibility(url_path):
    res, catgry = modify_route_visibility(url_path)
    flash(res, catgry)
    return jsonify({"message": res, "redirect": url_for('main.admin')})

@bp.route('/delete_route/<path:url_path>', methods=['GET'])
@login_required
def delete_route(url_path):
    res, catgry = remove_route(url_path)
    flash(res, catgry)
    return jsonify({"message": res, "redirect": url_for('main.admin')})

@bp.route('/<path:dynamic_path>')
def dynamic_handler(dynamic_path):
    return render_route(dynamic_path)

@bp.route('/fetch_payload/<path:url_path>', methods=['GET'])
@login_required
def fetch_payload(url_path):
    return jsonify({"payload": fetch_route_payload(url_path)})

@bp.route('/find_route', methods=['GET'])
@login_required
def find_route():
    search_field = request.args.get('query', '')
    return render_template('breach/admin.html', username=current_user.username, route_list=search_route(search_field=search_field))