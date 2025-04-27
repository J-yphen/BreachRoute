from flask import Blueprint, redirect, render_template, request, url_for
from ..models import AppConfig
from .. import db

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/admin')
def admin():
    config = AppConfig.query.first()

    if not config.setup_complete:
        return redirect(url_for('onboarding.setup'))

    return render_template('breach/admin.html')
    