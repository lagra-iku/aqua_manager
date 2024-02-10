#!/usr/bin/python3
"""Module that creates a flaskapp"""
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime
from configparser import ConfigParser
from werkzeug.security import generate_password_hash, check_password_hash
from users import User
import mysql.connector

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

db = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password']
)

app.secret_key = config['flash']['secret_key']
curr_date = datetime.now().strftime("%d-%b-%Y %I:%M %p")
cursor = db.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS requests")
cursor.execute("USE requests")

# Create tables if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        location VARCHAR(255),
        phonenum VARCHAR(30),
        bottle_qty INT,
        sachet_qty INT,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        modified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(255) DEFAULT 'New'
    )
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS production_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bottle_qty INT,
        sachet_qty INT,
        factory_worker VARCHAR(255),
        production_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        full_name VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
        date_modified DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get("username")
    if request.method == 'POST':
        bottle_qty = request.form['bottle_qty']
        sachet_qty = request.form['sachet_qty']
        name = request.form['name']
        location = request.form['location']
        phonenum = request.form['phonenum']

        # Insert data into MySQL
        cursor.execute("INSERT INTO requests (name, location, phonenum, bottle_qty, sachet_qty) VALUES (%(name)s, %(location)s, %(phonenum)s, %(bottle_qty)s, %(sachet_qty)s)",
                       {'name': name, 'location': location, 'phonenum': phonenum, 'bottle_qty': bottle_qty, 'sachet_qty': sachet_qty})
        db.commit()

        flash('Request submitted successfully!!!')
        return redirect(url_for('display_entry', id=cursor.lastrowid, username=username))
    return render_template('request/new.html', username=username, curr_date=datetime.now().strftime("%d-%b-%Y %I:%M %p"))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    username = session.get("username")
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        phonenum = request.form.get('phonenum')
        bottle_qty = request.form.get('bottle_qty')
        sachet_qty = request.form.get('sachet_qty')
        status = request.form.get('status')
        # Update data in MySQL
        cursor.execute(
            "UPDATE requests SET name = %s, location = %s, phonenum = %s, bottle_qty = %s, sachet_qty = %s, "
            "status = %s WHERE id = %s",
            (name, location, phonenum, bottle_qty, sachet_qty, status, id))
        db.commit()
        flash('Request updated successfully!!!')
        return redirect(url_for('display_entry', id=id, username=username))
    return render_template('request/edit.html', x=entry, curr_date=curr_date, username=username)


@app.route('/display/<int:id>', methods=['GET', 'POST'])
def display_entry(id,):
    username = session.get("username")
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    user_phonenum = entry[3]
    modified = entry[7]

    cursor.execute(
        "SELECT id, bottle_qty, sachet_qty, status, modified_date FROM requests WHERE phonenum = %s ORDER BY "
        "modified_date DESC",
        (user_phonenum,))
    req_history = cursor.fetchall()

    return render_template('request/display.html', x=entry, req=req_history, curr_date=curr_date, modified=modified, username=username)


@app.route('/dashboard')
def dashboard():
    username = session.get("username")
    cursor.execute(
        "SELECT id, name, location, phonenum, status FROM requests WHERE status  <> 'canceled' AND status <> "
        "'delivered' ORDER BY modified_date DESC")
    entry = cursor.fetchall()
    cursor.execute("""
    SELECT 
        SUM(CASE WHEN status = 'New' THEN 1 ELSE 0 END) AS new_count,
        SUM(CASE WHEN status = 'On route' THEN 1 ELSE 0 END) AS enroute_count,
        SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS completed_count,
        SUM(CASE WHEN status = 'Canceled' THEN 1 ELSE 0 END) AS canceled_count
    FROM requests
    """)

    # Fetch the result
    result = cursor.fetchone()

    # Extract counts for each status
    new_count = result[0]
    enroute_count = result[1]
    completed_count = result[2]
    canceled_count = result[3]

    cursor.execute("SELECT SUM(bottle_qty) AS bottle_sum FROM production_records")
    bottle = cursor.fetchone()
    bottle_sum = bottle[0]

    cursor.execute("SELECT SUM(sachet_qty) AS sachet_sum FROM production_records")
    sachet = cursor.fetchone()
    sachet_sum = sachet[0]
    return render_template('dashboard.html', x=entry, curr_date=curr_date, new=new_count, enroute=enroute_count,
                           completed=completed_count, canceled=canceled_count, bottled=bottle_sum, sachet=sachet_sum, username=username)


@app.route('/admin', methods=('GET', 'POST'))
def admin():
    fullname = session.get("full_name")
    cursor.execute(
        "SELECT id, name, bottle_qty, sachet_qty, status, modified_date FROM requests WHERE status  <> 'canceled' AND "
        "status <> 'completed' ORDER BY modified_date DESC")
    entry = cursor.fetchall()
    username = session.get("username")
    return render_template('admin/home.html', x=entry, fullname=fullname, username=username, curr_date=curr_date)


@app.route('/add_production', methods=['GET', 'POST'])
def add_production():
    username = session.get("username")
    fullname = session.get("full_name")
    if request.method == 'POST':
        bottle_qty = request.form.get('bottle_qty')
        sachet_qty = request.form.get('sachet_qty')
        factory_worker = request.form.get('factory_worker')
        production_date = request.form.get('production_date')
        # Insert the new production data into the production_records table
        cursor.execute(
            "INSERT INTO production_records (bottle_qty, sachet_qty, factory_worker, production_date) VALUES (%s, %s, "
            "%s, %s)",
            (bottle_qty, sachet_qty, factory_worker, production_date))
        db.commit()
        # Redirect to a success page
        flash('Production form submitted successfully!!!')
        # username = session.get("username")
        return redirect(url_for('production_content', username=username, fullname=fullname))

    return render_template('admin/add_production.html', curr_date=curr_date, username=username, fullname=fullname)


# @app.route('/view_analytics', methods=['GET', 'POST'])
# def view_analytics():
#     return redirect(url_for('dashboard', curr_date=curr_date))


@app.route('/production_content', methods=['GET', 'POST'])
def production_content():
    fullname = session.get("full_name")
    username = session.get("username")
    # Fetch production content data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM production_records ORDER BY production_date DESC")
    production_content_data = cursor.fetchall()
    # print(production_content_data)
    return render_template('admin/production_content.html', production_content_data=production_content_data, fullname=fullname,
                           curr_date=curr_date, username=username)


@app.route('/edit_production/<int:id>', methods=['GET', 'POST'])
def edit_production(id):
    username = session.get("username")
    cursor.execute("SELECT * FROM production_records WHERE id = %s", (id,))
    product_edit = cursor.fetchone()
    if request.method == 'POST':
        bottle_qty = request.form.get('bottle_qty')
        sachet_qty = request.form.get('sachet_qty')
        factory_worker = request.form.get('factory_worker')
        production_date = request.form.get('production_date')
        cursor.execute(
            "UPDATE production_records SET bottle_qty = %s, sachet_qty = %s, factory_worker = %s, production_date = "
            "%s WHERE id = %s",
            (bottle_qty, sachet_qty, factory_worker, production_date, id))
        db.commit()
        # db.close()
        flash('Production details updated successfully!!!')
        return redirect(url_for('production_content', username=username))
    return render_template('admin/edit_production.html', x=product_edit, curr_date=curr_date, username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        raw_password = request.form.get('password') 
        second_password = request.form.get("enter_password_again")
        full_name = request.form.get('full_name')
        
        if second_password != raw_password:
            flash('Passwords are different, please make sure they match.', 'error')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(raw_password)

            # Check if username is already taken
            cursor.execute("SELECT * FROM user_profiles WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username Taken! Please choose another one.', 'error')
                return redirect(url_for('register'))
            else:
                # Insert new user record into the database with hashed password
                cursor.execute("INSERT INTO user_profiles (username, email, password, full_name) VALUES (%s, %s, %s, %s)",
                           (username, email, hashed_password, full_name))
                db.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            # Consume flashed messages to ensure they are removed
                flashed_messages = get_flashed_messages(with_categories=True)
                if flashed_messages:
                    for category, message in flashed_messages:
                        pass  # Do nothing, just consume the flashed messages

    return render_template('user_profile/register.html', curr_date=curr_date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database to retrieve the user's data
        cursor.execute("SELECT id, username, password FROM user_profiles WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if a user with the provided username exists in the database
        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            session['username'] = username
            # Redirect to the user's profile page after successful login
            return redirect(url_for('admin', username=username))
            # return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('user_profile/login.html', curr_date=curr_date)


@app.route('/profile/<username>')
def profile(username):
    # Query the database to retrieve additional user information
    cursor.execute("SELECT email, full_name FROM user_profiles WHERE username = %s", (username,))
    user_info = cursor.fetchone()

    if user_info:
        email = user_info[0]
        full_name = user_info[1]
        session['full_name'] = full_name
        return render_template('user_profile/profile.html', username=username, email=email, full_name=full_name)
    else:
        flash('User not found', 'error')
        return redirect(url_for('login'))

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database to retrieve the user's data
        cursor.execute("SELECT id, username, password FROM user_profiles WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Check if a user with the provided username exists in the database
        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            print("Login was Successful")
            # Redirect to the admin page after successful login
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'error')
            print("login was unsuccessful!")
            return redirect(url_for('login'))

    return render_template('user_profile/login.html', curr_date=curr_date)



@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve user data from the database
    user_id = session['user_id']
    cursor.execute("SELECT username, email FROM user_profiles WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    return render_template('user_profile/profile.html', user_data=user_data)
"""

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    if request.method == 'GET':
        logout_user()
        flash('Logout successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('user_profile/login.html', curr_date=curr_date)


# Define route for 404 error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('503.html', error=error), 503


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)