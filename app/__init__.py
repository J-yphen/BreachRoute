from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
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
    
    from .breach_route import bp as main_bp
    from .onboarding import bp as onboarding_bp
    
    app.register_blueprint(main_bp)
    if not app.config['SETUP_COMPLETE']:
        app.register_blueprint(onboarding_bp)
        # app.add_url_rule('/', endpoint='onboarding.setup') ### Adding this will redirect to `/setup` by default

    return app

app = create_app()
