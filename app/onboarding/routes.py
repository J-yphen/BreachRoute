from app.service.services import StorageService
from .. import db
from ..models import AppConfig, User
from werkzeug.security import generate_password_hash
from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app

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
        provider_type = request.form.get('provider-type')

        # url_path = request.form.get('url_path')

        if 'username' not in request.form and 'password'not in request.form:
            flash("Invalid username or password", "error")
            return render_template('onboarding/setup.html')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username or path already exists", "error")
            return render_template('onboarding/setup.html')
        
        if request.form.get('setup_s3') == 'enabled':
            required_fields = []
            if provider_type == "aws":
                required_fields = ['access_key', 'secret_key', 'bucket_name', 'region_name', 'endpoint_url']
            elif provider_type == "gcp":
                required_fields = ['access_key', 'secret_key', 'bucket_name']
            elif provider_type == "azure":
                required_fields = ['access_key', 'secret_key', 'bucket_name']
            elif provider_type == "digitalocean":
                required_fields = ['access_key', 'secret_key', 'bucket_name', 'region_name']
            elif provider_type == "backblaze":
                required_fields = ['access_key', 'secret_key', 'bucket_name']
            else:
                required_fields = ['access_key', 'secret_key', 'bucket_name', 'region_name', 'endpoint_url']

            for field in required_fields:
                if not request.form.get(field):
                    flash("All fields are required", "error")
                    return render_template('onboarding/setup.html')
            
        config.provider_type = provider_type
        config.s3_access_key = request.form.get('access_key')
        config.s3_secret_key = request.form.get('secret_key')
        config.s3_bucket_name = request.form.get('bucket_name')
        config.s3_region_name = request.form.get('region_name')
        config.s3_url = request.form.get('endpoint_url')
        
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        config.setup_complete = True
        db.session.commit()
        flash("Setup has been completed successfully", "success")

        current_app.config['PROVIDER_TYPE'] = config.provider_type
        current_app.config['S3_ACCESS_KEY'] = config.s3_access_key
        current_app.config['S3_SECRET_KEY'] = config.s3_secret_key
        current_app.config['S3_BUCKET_NAME'] = config.s3_bucket_name
        current_app.config['S3_REGION'] = config.s3_region_name
        current_app.config['S3_ENDPOINT_URL'] = config.s3_url

        current_app.storage_service = StorageService(config.provider_type)
        return redirect(url_for('main.login_handler'))

    return render_template('onboarding/setup.html')