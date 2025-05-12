import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.service.services import StorageService

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.ProductionConfig'):
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
        
    from . import models

    with app.app_context():
        db.create_all()
        from .models import AppConfig
        config = AppConfig.query.first()
        
        if not config:
            config = AppConfig(setup_complete=False)
            db.session.add(config)
            db.session.commit()
        
        app.config['SETUP_COMPLETE'] = config.setup_complete
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        if config.setup_complete:
            app.config['PROVIDER_TYPE'] = config.provider_type
            app.config['S3_ACCESS_KEY'] = config.s3_access_key
            app.config['S3_SECRET_KEY'] = config.s3_secret_key
            app.config['S3_BUCKET_NAME'] = config.s3_bucket_name
            app.config['S3_REGION'] = config.s3_region_name
            app.config['S3_ENDPOINT_URL'] = config.s3_url

            app.storage_service = StorageService(app.config['PROVIDER_TYPE'])
    
    from .breach_route import bp as main_bp
    from .onboarding import bp as onboarding_bp
    
    app.register_blueprint(main_bp)
    if not app.config['SETUP_COMPLETE']:
        app.register_blueprint(onboarding_bp)
        # app.add_url_rule('/', endpoint='onboarding.setup') ### Adding this will redirect to `/setup` by default

    from flask import render_template
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login_handler'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

app = create_app()
