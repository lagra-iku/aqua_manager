#!/usr/bin/python3
"""Module that creates a flaskapp"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, timedelta
import mysql.connector

app = Flask(__name__)

curr_date = datetime.now().strftime("%d-%b-%Y %I:%M %p")

db = mysql.connector.connect(
    host="127.0.0.1",
    user="lagra",
    password="root"
)

cursor = db.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS requests")
cursor.execute("USE requests")

# Create tables if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS requests (id  INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR (255), location VARCHAR (255), phonenum VARCHAR (30), bottle_qty INT(11), sachet_qty INT(11), created_date DATETIME DEFAULT CURRENT_TIMESTAMP, modified_date DATETIME DEFAULT CURRENT_TIMESTAMP, status VARCHAR (255) DEFAULT 'New', PRIMARY KEY(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS production_records (id INT(11) NOT NULL AUTO_INCREMENT, product_name VARCHAR(255), factory_worker VARCHAR(255), quantity INT, production_date DATE, PRIMARY KEY(id))")

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
       bottle_qty = request.form['bottle_qty']
       sachet_qty = request.form['sachet_qty']

        # Update data in MySQL
       cursor.execute("UPDATE requests SET name = %s, location = %s, phonenum = %s, bottle_qty = %s, sachet_qty = %s WHERE id = %s", (name, location, phonenum, bottle_qty, sachet_qty, id))
       db.commit()
       return redirect(url_for('display_entry', id=id))
    return render_template('request/edit.html', x=entry, curr_date=curr_date)

@app.route('/display/<int:id>', methods=['GET', 'POST'])
def display_entry(id):
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    user_phonenum = entry[3]
    modified = entry[7].strftime("%d-%b-%Y at %I:%M %p")

    cursor.execute("SELECT bottle_qty, sachet_qty, modified_date FROM requests WHERE phonenum = %s ORDER BY modified_date DESC", (user_phonenum,))
    req_history = cursor.fetchall()

    return render_template('request/display.html', x=entry, req=req_history, curr_date=curr_date, modified=modified)


@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT id, name, location, phonenum, status FROM requests")
    entry = cursor.fetchall()
    return render_template('dashboard.html', x=entry, curr_date=curr_date)

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    return render_template('admin/home.html', curr_date=curr_date)

@app.route('/add_production', methods=['GET', 'POST'])
def add_production():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        factory_worker = request.form.get('factory_worker')
        # Get the current date
        production_date = datetime.now().date()
        # Insert the new production data into the production_records table
        cursor.execute("INSERT INTO production_records (product_name, quantity, factory_worker, production_date) VALUES (%s, %s, %s, %s)", (product_name, quantity, factory_worker, production_date))
        db.commit()

        # Redirect to a success page or any other page
        return redirect(url_for('add_production'))

    return render_template('admin/add_production.html', curr_date=curr_date)

@app.route('/view_analytics', methods=['GET', 'POST'])
def view_analytics():
    return redirect(url_for('dashboard', curr_date=curr_date))

@app.route('/production_content', methods=['GET', 'POST'])
def production_content():
    # Fetch production content data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM production_records")
    production_content_data = cursor.fetchall()
    # print(production_content_data)
    return render_template('admin/production_content.html', production_content_data=production_content_data, curr_date=curr_date)

@app.route('/edit_production/<int:id>', methods=['GET', 'POST'])
def edit_production(id):
    cursor.execute("SELECT * FROM production_records WHERE id = %s", (id,))
    product_edit = cursor.fetchone()
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        factory_worker = request.form.get('factory_worker')
        production_date = datetime.now().date()
        cursor.execute("UPDATE production_records SET product_name = %s, quantity = %s, factory_worker = %s, production_date = %s WHERE id = %s", (product_name, quantity, factory_worker, production_date, id))
        db.commit()
       # db.close()
        return redirect(url_for('production_content'))
    return render_template('admin/edit_production.html', x=product_edit, curr_date=curr_date)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)