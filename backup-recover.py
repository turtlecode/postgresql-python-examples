'''
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com'),
('Diana', 'diana@example.com'),
('Ethan', 'ethan@example.com');

select * from users;

delete from users;
'''

#backup 

import subprocess
import os

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "turtlecode"
DB_HOST = "localhost"
DB_PORT = "5432"

BACKUP_FILE = "users_backup.sql"

os.environ["PGPASSWORD"] = DB_PASSWORD

subprocess.run(
    [
        "pg_dump",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-t", "users",
        "-f", BACKUP_FILE
    ],
    check=True
)

print("Backup completed successfully.")


#recover
import subprocess
import os

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "turtlecode"
DB_HOST = "localhost"
DB_PORT = "5432"

BACKUP_FILE = "users_backup.sql"

os.environ["PGPASSWORD"] = DB_PASSWORD

subprocess.run(
    [
        "psql",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", BACKUP_FILE
    ],
    check=True
)

print("Restore completed successfully.")
