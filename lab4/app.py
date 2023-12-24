import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="18012004",
    host="localhost",
    port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not bool(username) or not bool(password):
        return render_template('account.html', error=2)
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if len(records):
        return render_template('account.html', data=', '.join(records[0][1:]))
    else:
        return render_template('account.html', error=1)
