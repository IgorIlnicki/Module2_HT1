-- Create table for status
DROP TABLE IF EXISTS status0;
CREATE TABLE status0 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
-- Create table for users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
-- Insert default statuses
--INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed');

-- Create table for tasks
DROP TABLE IF EXISTS tasks
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status0(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
--ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
--ALTER TABLE status ADD CONSTRAINT unique_name UNIQUE (name);