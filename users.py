import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))

    def __init__(self, username, password, email, full_name=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.set_password(password)

    def set_password(self, password):
        # Generate password hash using bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def save_to_database(self):
        # Add the user instance to the database session and commit the transaction
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def login(username, password):
        # Query the database to retrieve the user's data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return user 
        else:
            return None

    @staticmethod
    def get_profile(user_id):
        # Retrieve user data from the database
        return User.query.get(user_id)

    @staticmethod
    def is_username_available(username):
        # Check if the username is already in use
        return User.query.filter_by(username=username).first() is None

    @staticmethod
    def logout():
        pass
