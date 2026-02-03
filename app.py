from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, bcrypt, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register Blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from routes.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from routes.match import match as match_blueprint
    app.register_blueprint(match_blueprint)

    from routes.connection import connection as connection_blueprint
    app.register_blueprint(connection_blueprint)

    from routes.blind_date import blind_date as blind_date_blueprint
    app.register_blueprint(blind_date_blueprint)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
