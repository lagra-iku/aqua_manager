#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def request():
    return render_template('request/new.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
