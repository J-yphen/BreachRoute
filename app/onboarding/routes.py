from .. import db
from ..models import AppConfig, User
from werkzeug.security import generate_password_hash
from flask import Blueprint, flash, render_template, redirect, url_for, request

bp = Blueprint('onboarding', __name__,
              template_folder='templates')

@bp.route('/setup', methods=['GET', 'POST'])
def setup():
    config = AppConfig.query.first()
    
    if config.setup_complete:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # url_path = request.form.get('url_path')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username or path already exists", "error")
            return render_template('onboarding/setup.html')
        
        new_user = User(username=username, password=generate_password_hash(password))

        db.session.add(new_user)
        config.setup_complete = True
        db.session.commit()
        flash("Setup has been completed successfully", "success")
        return redirect(url_for('main.login_handler'))

    return render_template('onboarding/setup.html')