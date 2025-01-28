from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db
from datetime import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Инициализация базы данных
init_db()


# Функция для получения соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('cleaner.db')
    conn.row_factory = sqlite3.Row
    return conn


# Главная страница
@app.route('/')
def index():
    return render_template('login.html')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin', 0)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                           (username, password, is_admin))
            conn.commit()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Пользователь с таким именем уже существует!', 'error')
        finally:
            conn.close()

    return render_template('register.html')


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user != None:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            if user['is_admin']:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user'))
        else:
            flash('Неверное имя пользователя или пароль!', 'error')

    return render_template('login.html', today=date.today())


# Выход
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Страница пользователя
@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'user_id' not in session or session['is_admin']:
        return redirect(url_for('login'))

    return render_template('user.html')


# Страница админа
@app.route('/admin')
def admin():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    return render_template('admin.html')



if __name__ == "__main__":
    app.run(debug=True)