import re
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
        return redirect(url_for('main.admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        url_path = request.form.get('url_path')
        
        user = User.query.filter_by(username=username).first()
        if user or not bool(re.fullmatch(r'[A-Za-z0-9_-]+', url_path)) or url_path == "admin":
            flash('Username or path already exists')
            return render_template('onboarding/setup.html')
        
        new_user = User(username=username, url_path=url_path, password=generate_password_hash(password))

        db.session.add(new_user)
        config.setup_complete = True
        db.session.commit()
        return redirect(url_for('main.admin'))

    return render_template('onboarding/setup.html')
