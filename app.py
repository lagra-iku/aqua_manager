#!/usr/bin/python3
"""Module that creates a flaskapp"""
from configparser import ConfigParser
from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import datetime
import mysql.connector

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

db = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password']
)

app.secret_key = config['flash']['secret_key']
curr_date = datetime.now().strftime("%d-%b-%Y %I:%M %p")
cursor = db.cursor()

# Create database if not existsgi t
cursor.execute("CREATE DATABASE IF NOT EXISTS requests")
cursor.execute("USE requests")

# Create tables if not exists
<<<<<<< HEAD
cursor.execute("CREATE TABLE IF NOT EXISTS requests (id  INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR (255), location VARCHAR (255), phonenum VARCHAR (30), bottle_qty INT(11), sachet_qty INT(11), created_date DATETIME DEFAULT CURRENT_TIMESTAMP, modified_date DATETIME DEFAULT CURRENT_TIMESTAMP, status VARCHAR (255) DEFAULT 'New', PRIMARY KEY(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS production_records (id INT(11) NOT NULL AUTO_INCREMENT, bottle_qty INT(11), sachet_qty INT(11), factory_worker VARCHAR(255), production_date DATETIME DEFAULT CURRENT_TIMESTAMP, created_date DATETIME DEFAULT CURRENT_TIMESTAMP, modified_date DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))")
=======
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
>>>>>>> 29200383d326c376202a01f6e47a5987ba0ccb3e


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        bottle_qty = request.form['bottle_qty']
        sachet_qty = request.form['sachet_qty']
        name = request.form['name']
        location = request.form['location']
        phonenum = request.form['phonenum']

        # Insert data into MySQL
        cursor.execute("INSERT INTO requests (name, location, phonenum, bottle_qty, sachet_qty) VALUES (%s, %s, %s, %s, %s)", (name, location, phonenum, bottle_qty, sachet_qty))
        db.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        flash('Request submitted successfully!!!')
        return redirect(url_for('display_entry', id=last_id))
    return render_template('request/new.html', curr_date=curr_date)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
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
       cursor.execute("UPDATE requests SET name = %s, location = %s, phonenum = %s, bottle_qty = %s, sachet_qty = %s, status = %s WHERE id = %s", (name, location, phonenum, bottle_qty, sachet_qty, status, id))
       db.commit()
       flash('Request updated successfully!!!')
       return redirect(url_for('display_entry', id=id))
    return render_template('request/edit.html', x=entry, curr_date=curr_date)

@app.route('/display/<int:id>', methods=['GET', 'POST'])
def display_entry(id):
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    user_phonenum = entry[3]
    modified = entry[7]

    cursor.execute("SELECT id, bottle_qty, sachet_qty, status, modified_date FROM requests WHERE phonenum = %s ORDER BY modified_date DESC", (user_phonenum,))
    req_history = cursor.fetchall()

    return render_template('request/display.html', x=entry, req=req_history, curr_date=curr_date, modified=modified)


@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT id, name, location, phonenum, status FROM requests WHERE status  <> 'canceled' AND status <> 'delivered' ORDER BY modified_date DESC")
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
    return render_template('dashboard.html', x=entry, curr_date=curr_date, new=new_count, enroute=enroute_count, completed=completed_count, canceled=canceled_count, bottled=bottle_sum, sachet=sachet_sum)

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    cursor.execute("SELECT id, name, bottle_qty, sachet_qty, status, modified_date FROM requests WHERE status  <> 'canceled' AND status <> 'completed' ORDER BY modified_date DESC")
    entry = cursor.fetchall()
    return render_template('admin/home.html', x=entry, curr_date=curr_date)

@app.route('/add_production', methods=['GET', 'POST'])
def add_production():
    if request.method == 'POST':
        bottle_qty = request.form.get('bottle_qty')
        sachet_qty = request.form.get('sachet_qty')
        factory_worker = request.form.get('factory_worker')
        production_date = request.form.get('production_date')
        # Insert the new production data into the production_records table
        cursor.execute("INSERT INTO production_records (bottle_qty, sachet_qty, factory_worker, production_date) VALUES (%s, %s, %s, %s)", (bottle_qty, sachet_qty, factory_worker, production_date))
        db.commit()

        # Redirect to a success page
        flash('Production form submitted successfully!!!')
        return redirect(url_for('production_content'))

    return render_template('admin/add_production.html', curr_date=curr_date)

@app.route('/view_analytics', methods=['GET', 'POST'])
def view_analytics():
    return redirect(url_for('dashboard', curr_date=curr_date))

@app.route('/production_content', methods=['GET', 'POST'])
def production_content():
    # Fetch production content data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM production_records ORDER BY production_date DESC")
    production_content_data = cursor.fetchall()
    # print(production_content_data)
    return render_template('admin/production_content.html', production_content_data=production_content_data, curr_date=curr_date)

@app.route('/edit_production/<int:id>', methods=['GET', 'POST'])
def edit_production(id):
    cursor.execute("SELECT * FROM production_records WHERE id = %s", (id,))
    product_edit = cursor.fetchone()
    if request.method == 'POST':
         bottle_qty = request.form.get('bottle_qty')
         sachet_qty = request.form.get('sachet_qty')
         factory_worker = request.form.get('factory_worker')
         production_date = request.form.get('production_date')
         cursor.execute("UPDATE production_records SET bottle_qty = %s, sachet_qty = %s, factory_worker = %s, production_date = %s WHERE id = %s", (bottle_qty, sachet_qty, factory_worker, production_date, id))
         db.commit()
       # db.close()
         flash('Production details updated successfully!!!')
         return redirect(url_for('production_content'))
    return render_template('admin/edit_production.html', x=product_edit, curr_date=curr_date)

<<<<<<< HEAD
@app.route('/login', methods=('GET', 'POST'))
=======

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get['username']
        email = request.form.get['email']
        password = request.form.get['password']
        full_name = request.form.get['full_name']

        # Check if username is available
        if not User.is_username_available(username):
            flash('Username Taken! Please choose another one.', 'error')
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(username, password, email, '')
        # Save the new user to the database
        new_user.save_to_database()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('user_profile/register.html', curr_date=curr_date)



@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/login', methods=['GET', 'POST'])
>>>>>>> 29200383d326c376202a01f6e47a5987ba0ccb3e
def login():
    return render_template('user_profile/login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)