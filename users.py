#!/usr/bin/python3
"""Module that handles user instances of registration, login and profiles"""
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
# from configparser import ConfigParser
# config = ConfigParser()
# config.read('config.ini')


# db = mysql.connector.connect(
#     host=config['mysql']['host'],
#     user=config['mysql']['user'],
#     password=config['mysql']['password']
# )

host = "MYSQLHOST"
user = "MYSQLUSER"
password = "MYSQLPASSWORD"
database = "MYSQLDATABASE"

try:
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connected successfully!")
    
cursor = db.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS requests")
cursor.execute("USE requests")

class User:
    def __init__(self, username, password, email, full_name):
        self.password_hash = None
        self.username = username
        self.email = email
        self.full_name = full_name
        self.set_password(password)

    def set_password(self, password):
        # Generate password hash using a secure hashing algorithm
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return check_password_hash(self.password_hash, password)

    def save_to_database(self):
        # Insert the user data into the MySQL database
        cursor.execute("INSERT INTO user_profiles (username, email, password) VALUES (%s, %s, %s)",
                       (self.username, self.email, self.password_hash))
        db.commit()

    @staticmethod
    def login(username, password):
        # Query the database to retrieve the user's data
        cursor.execute("SELECT id, username, password FROM user_profiles WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[2], password):
            return user_data[0]  # Return the user's ID
        else:
            return None

    @staticmethod
    def get_profile(user_id):
        # Retrieve user data from the database
        cursor.execute("SELECT username, email, full_name FROM user_profiles WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            return {
                'username': user_data[0],
                'email': user_data[1],
                'full_name': user_data[2]
            }
        else:
            return None
        
    @staticmethod
    def is_username_available(username):
        # Check if the username is already in use
        cursor.execute("SELECT id FROM user_profiles WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        return user_data is None 
    
    @staticmethod
    def logout():
        # Close the cursor
        cursor.close()
        # Close the database connection
        db.close()
