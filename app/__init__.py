from flask import Flask

def create_app(config_class='config.Config'):
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    app.config.from_object(config_class)
    
    from .breach_route import bp as main_bp
    from .onboarding import bp as onboarding_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(onboarding_bp)

    return app

app = create_app()
