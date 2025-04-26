from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint('onboarding', __name__)

@bp.route('/setup', methods=['GET', 'POST'])
def setup():
    return "SETUP"
