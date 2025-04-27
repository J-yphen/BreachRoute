from flask import Blueprint, render_template, redirect, url_for, request
from ..models import AppConfig
from .. import db

bp = Blueprint('onboarding', __name__,
              template_folder='templates')

@bp.route('/setup', methods=['GET', 'POST'])
def setup():
    config = AppConfig.query.first()
    
    if config.setup_complete:
        return redirect(url_for('main.admin'))

    if request.method == 'POST':
        config.setup_complete = True
        db.session.commit()
        return redirect(url_for('main.admin'))

    return render_template('onboarding/setup.html')
