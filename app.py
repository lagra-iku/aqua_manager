#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, timedelta
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="Olisajioke",
    password="@Lt@ir@@7"
)

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

        return redirect(url_for('dashboard'))
    return render_template('request/new.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
    entry = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        phonenum = request.form['phonenum']

        # Update data in MySQL
        cursor.execute("UPDATE requests SET name = %s, location = %s, phonenum = %s WHERE id = %s", (name, location, phonenum, id))
        db.commit()

        return redirect(url_for('dashboard'))
    return render_template('request/edit.html', entry=entry)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin', method=('GET', 'POST'))
def admin():
    customer_list = request
    return render_template('admin/home.html')

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

    return render_template('admin/add_production.html')

@app.route('/view_analytics', methods=['GET', 'POST'])
def view_analytics():
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)