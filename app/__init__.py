from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from alembic import command
from alembic.config import Config as AlembicConfig
from pathlib import Path

db = SQLAlchemy()
migrate = Migrate()

def run_migrations():
    base_dir = Path(__file__).parent.parent
    alembic_cfg = AlembicConfig(str(base_dir / 'migrations' / 'alembic.ini'))
    alembic_cfg.set_main_option('script_location', 'migrations')
    command.upgrade(alembic_cfg, 'head')

def create_app(config_class='config.Config'):
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Initialize database and run migrations
        if not (Path(__file__).parent.parent / 'migrations').exists():
            # Initialize Alembic migrations directory
            from flask_migrate import init as flask_migrate_init
            flask_migrate_init()
            # Generate initial migration script
            from flask_migrate import migrate as flask_migrate_migrate
            flask_migrate_migrate(message="Initial migration")
            # Stamp the database as up-to-date
            from flask_migrate import stamp as flask_migrate_stamp
            flask_migrate_stamp()
        
        # Apply migrations
        run_migrations()

    
    from .breach_route import bp as main_bp
    from .onboarding import bp as onboarding_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(onboarding_bp)

    return app

app = create_app()
