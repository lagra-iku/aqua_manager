from flask import Flask 
from models import db
from login_loader import init_app

def create_app():
    app = Flask(__name__)
    app.secret_key = 'aqua_manager_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Initialize the login manager
    init_app(app)

    # Import and register the blueprint
    from routes import main_bp
    app.register_blueprint(main_bp)

    # Create all database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
