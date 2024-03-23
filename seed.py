from faker import Faker
import psycopg2

fake = Faker()

# Connect to the database
conn = psycopg2.connect(
    dbname="your_database",
    user="your_username",
    password="your_password",
    host="localhost"
)
cur = conn.cursor()

# Populate users table
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Populate status table
status_names = ['new', 'in progress', 'completed']
for name in status_names:
    cur.execute("INSERT INTO status (name) VALUES (%s)", (name,))

# Populate tasks table
for _ in range(20):
    title = fake.text(max_nb_chars=100)
    description = fake.text()
    status_id = fake.random_int(min=1, max=len(status_names))
    user_id = fake.random_int(min=1, max=10)
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()