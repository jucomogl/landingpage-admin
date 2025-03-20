from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Setup
def setup_database():
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        email TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sections (
                        id INTEGER PRIMARY KEY,
                        type TEXT,
                        title TEXT,
                        author TEXT,
                        date TEXT,
                        content TEXT,
                        icon TEXT,
                        link TEXT)''')
    conn.commit()
    conn.close()
setup_database()

@app.route('/')
def home():
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sections")
    sections = cursor.fetchall()
    conn.close()
    return render_template('index.html', sections=sections)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('admin'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'user' in session:
        return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/add_section', methods=['POST'])
def add_section():
    if 'user' in session:
        section_type = request.form['type']
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']
        content = request.form['content']
        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sections (type, title, author, date, content) VALUES (?, ?, ?, ?, ?)",
                       (section_type, title, author, date, content))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
