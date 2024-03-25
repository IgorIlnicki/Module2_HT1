# import sqlite3

# def create_db():
# # читаємо файл зі скриптом для створення БД
#     with open('manager_tasks.sql', 'r') as f:
#         sql = f.read()

# # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
#     with sqlite3.connect('manager_tasks.db') as con:
#         cur = con.cursor()
# # виконуємо скрипт із файлу, який створить таблиці в БД
#         cur.executescript(sql)

# if __name__ == "__main__":
#     create_db()
import sqlite3

def create_tables():
    # Підключення до бази даних SQLite (створюється, якщо вона не існує)
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()

    # Створити таблицю БД users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    fullname VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                 )''')

    # Створити таблицю БД status
    c.execute('''CREATE TABLE IF NOT EXISTS status (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) UNIQUE
                 )''')

    # Вставити значення стану за замовчуванням
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('new')")
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('in progress')")
    c.execute("INSERT OR IGNORE INTO status (name) VALUES ('completed')")

    # Створити таблицю БД tasks
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(100),
                    description TEXT,
                    status_id INTEGER REFERENCES status(id),
                    user_id INTEGER REFERENCES users(id)
                 )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()