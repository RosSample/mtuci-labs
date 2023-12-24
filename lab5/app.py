import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="18012004",
    host="localhost",
    port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
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
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if not bool(name) or not bool(password) or not bool(login):
                return render_template('account.html', error=3)
        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) == 0:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
            conn.commit()
        else:
            return render_template('account.html', error=4)
        return redirect('/login/')
    return render_template('registration.html')