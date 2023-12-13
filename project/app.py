from flask import Flask, render_template, request, redirect, url_for, flash, session

import time
app = Flask(__name__)
app.secret_key = 'your_secret_key'


users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username 
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index2.html')
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
