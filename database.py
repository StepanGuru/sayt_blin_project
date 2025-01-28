import sqlite3


def init_db():
    conn = sqlite3.connect('cleaner.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS users''')

    # Создаем таблицу пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  is_admin BOOLEAN NOT NULL DEFAULT 0)''')


    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()