from flask import Flask
from models import db
from routes import main_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'aqua_manager_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
