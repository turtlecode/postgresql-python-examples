'''
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    balance INTEGER
);

INSERT INTO accounts (balance) VALUES (100);

select * from accounts;

SET lock_timeout = '1s';
UPDATE accounts
SET balance = balance - 20
WHERE id = 1;

'''

import psycopg2
import time

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="turtlecode"
)

conn.autocommit = False
cursor = conn.cursor()

print("Transaction A: updating row...")

cursor.execute("""
    UPDATE accounts
    SET balance = balance + 50
    WHERE id = 1;
""")

print("Transaction A: holding the lock for 10 seconds...")
time.sleep(10)

conn.commit()
print("Transaction A: commit completed")

cursor.close()
conn.close()
