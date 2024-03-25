import sqlite3

def get_tasks_not_completed():  # 6  отримати завдання, статус яких не "виконано"
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання, статус яких не "виконано"
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks
        WHERE status_id != (
            SELECT id
            FROM status
            WHERE name = 'completed'
        )
    """)
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task(title, description, status_id, user_id): # 5 Додати нове завдання для конкретного користувача
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит, щоб вставити нове завдання
    c.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, ?, ?)
    """, (title, description, status_id, user_id))
    conn.commit()
    conn.close()


def get_users_without_tasks(): # 4 отримати список користувачів, які не мають жодних завдань.
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати список користувачів, які не мають жодних завдань.
    c.execute("""
        SELECT id, fullname
        FROM users
        WHERE id NOT IN (
            SELECT DISTINCT user_id
            FROM tasks
        )
    """)
    users = c.fetchall()
    conn.close()
    return users

def update_task_status(task_id, new_status):   # 3 запит для оновлення статусу певного завдання
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит для оновлення статусу певного завдання
    c.execute("""
        UPDATE tasks
        SET status_id = (
            SELECT id
            FROM status
            WHERE name = ?
        )
        WHERE id = ?
    """, (new_status, task_id))
    conn.commit()  # оновлюємо
    conn.close()

def get_tasks_by_status(status_name):  # 2  отримати завдання з певним статусом
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання з певним статусом
    c.execute("""
        SELECT tasks.id, tasks.title, tasks.description, users.fullname
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE tasks.status_id = (
            SELECT id
            FROM status
            WHERE name = ?
        )
    """, (status_name,))
    tasks = c.fetchall()
    conn.close()

    return tasks

def get_tasks_by_user_id(user_id):  # 1 отримати завдання певного користувача за його ідентифікатором
    conn = sqlite3.connect('task_management.db')
    c = conn.cursor()
    # SQL-запит, щоб отримати завдання певного користувача за його ідентифікатором
    c.execute("""SELECT tasks.id, tasks.title, tasks.description, users.fullname, status.name AS status_name
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        JOIN status ON tasks.status_id = status.id
        WHERE tasks.user_id = ?
    """, (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def pripe_get_tasks_not_completed():   # 6
    tasks = get_tasks_not_completed()
    if tasks:
        print("Завдання, статус яких не <виконано>:")
        for task in tasks:
            print(task)
    else:
        print("Не знайдено завдань зі статусом, відмінним від <виконано>.")

def pripe_add_task():  # 5
    title = "Complete project"
    description = "Finish the final report and submit it by Friday."
    status_id = 1  # Тут можна замінити 1 відповідним ідентифікатором статусу
    user_id = 1  # Тут можна замінити 1 ідентифікатором конкретного користувача, для якого призначено завдання
    add_task(title, description, status_id, user_id)
    print("Додано нове завдання для користувача з ID {}.".format(user_id))

def pripe_get_users_without_tasks():   # 4
    users = get_users_without_tasks()
    if users:
        print("Користувачі, які не мають жодних завдань:")
        for user in users:
            print(user)
    else:
        print("У всіх користувачів є завдання.")

def pripe_update_task_status(args):   # 3
    task_id = int(args[0]) 
    if len(args) == 3:
        new_status = "in progress"
    else:
        new_status = args[1]
    print(f"  task_id = {task_id} new_status = {new_status}")
    update_task_status(task_id, new_status)
    print("Статус завдання з ідентифікатором {} змінено на: '{}'.".format(task_id, new_status))

def pripe_execute_by_status(args):  #2
    status_name = args[0]
    tasks = get_tasks_by_status(status_name)
    if tasks:
        print("Вибрати завдання зі статусом: {}: ".format(status_name))  
        i = 0
        for task in tasks:
            #print(f"   task: {task}")
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]} \n   Ім'я користувача: {task[3]}")
            i +=1
    else:
        print("No tasks found for user with ID {}.".format(status_name))

def pripe_get_tasks_by_user_id(args):   #1
    user_id = int(args[0])   # конкретний ідентифікатор користувача, для якого треба отримати завдання
    tasks = get_tasks_by_user_id(user_id)
    if tasks:
        print("Завдання для користувача з Id: {}: ".format(user_id))  
        i = 0
        for task in tasks:
            if i == 0:
                print(f"Ім'я користувача: {task[3]}")
            print(f"{i+1}.\n   Номер задачі: {task[0]}")
            print(f"   Назва задачі: {task[1]} \n   Опис задачі:\n{task[2]} \n   Статус: {task[4]}")
            i +=1

    else:
        print("No tasks found for user with ID {}.".format(user_id))

def parse_input(user_input): # ввод команди та аргументів
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    print("Ласкаво просимо до бота-помічника!")
    print("Формат команд:\nclose або exit\nSelect [user_id]\nExecute [status_name]\nUpdate [task_id] [new_status]\nGet") 
    print("Get_users_without_tasks\nAdd_task\nGet_tasks_not_completed")
    while True: 
            user_input = input("Введіть команду: ")
            command, *args = parse_input(user_input)
            # print(f"   cmd = {command}    args[0] = {args[0]}")
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "select":  # 1
               pripe_get_tasks_by_user_id(args)
            elif command == "execute":  # 2
               pripe_execute_by_status(args)
            elif command == "update":  # 3
               pripe_update_task_status(args)
            elif command == "get_users_without_tasks":  # 4
                pripe_get_users_without_tasks()
            elif command == "add_task":  # 5
                pripe_add_task()
            elif command == "get_tasks_not_completed":  # 6
                pripe_get_tasks_not_completed()

if __name__ == "__main__":
    main()