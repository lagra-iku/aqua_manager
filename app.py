#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, timedelta
import mysql.connector

app = Flask(__name__)


# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="lagra",
    password="root",
    database="requests"
)
cursor = db.cursor()

# Create table if not exists
cursor.execute("CREATE TABLE IF NOT EXISTS requests (id  INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR (255), location VARCHAR (255), phonenum VARCHAR (30), PRIMARY KEY(id))")


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
       name = request.form.get['name']
       location = request.form.get['location']
       phonenum = request.form.get['phonenum']

        # Update data in MySQL
       cursor.execute("UPDATE requests SET name = %s, location = %s, phonenum = %s WHERE id = %s", (name, location, phonenum, id))
       db.commit()
       db.close()
       return "updated successfully"
    return render_template('request/edit.html', x=entry)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    return render_template('admin/home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
