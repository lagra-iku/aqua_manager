#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, timedelta
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="127.0.0.1",
    user="",
     password=""
)
# Connect to MySQL
if not db.is_connected():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="",
        password=""
    )

curr_date = datetime.now().strftime("%d-%b-%Y %I:%M %p")
cursor = db.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS requests")
cursor.execute("USE requests")

# Create tables if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS requests (id  INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR (255), location VARCHAR (255), phonenum VARCHAR (30), PRIMARY KEY(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS production_records (id INT(11) NOT NULL AUTO_INCREMENT, product_name VARCHAR(255), quantity INT, production_date DATE, PRIMARY KEY(id))")

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        phonenum = request.form['phonenum']

        # Insert data into MySQL
        cursor.execute("INSERT INTO requests (name, location, phonenum) VALUES (%s, %s, %s)", (name, location, phonenum))
        db.commit()

        return redirect(url_for('display_entries'))
    return render_template('request/new.html', curr_date=curr_date)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    if request.method == 'POST':
       name = request.form.get('name')
       location = request.form.get('location')
       phonenum = request.form.get('phonenum')

        # Update data in MySQL
       cursor.execute("UPDATE requests SET name = %s, location = %s, phonenum = %s WHERE id = %s", (name, location, phonenum, id))
       db.commit()
       # db.close()
       return redirect(url_for('display_entries'))
    return render_template('request/edit.html', x=entry, curr_date=curr_date)

@app.route('/requests', methods=['GET', 'POST'])
def display_entries():
    cursor.execute("SELECT * FROM requests")
    entry = cursor.fetchall()
    return render_template('request/display.html', x=entry, curr_date=curr_date)


@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM requests")
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

        # Get the current date
        production_date = datetime.now().date()

        # Insert the new production data into the production_records table
        cursor.execute("INSERT INTO production_records (product_name, quantity, production_date) VALUES (%s, %s, %s)", (product_name, quantity, production_date))
        db.commit()

        # Redirect to a success page or any other page
        return redirect(url_for('add_production'))

    return render_template('admin/add_production.html', curr_date=curr_date)

@app.route('/view_analytics', methods=['GET', 'POST'])
def view_analytics():
    return redirect(url_for('dashboard', curr_date=curr_date))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)