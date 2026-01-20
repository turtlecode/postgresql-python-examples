'''
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    balance INT
);

INSERT INTO accounts VALUES
(1, 1000),
(2, 1000);

select * from accounts;

'''

import psycopg2
import threading
import time

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "turtlecode",
    "host": "localhost",
    "port": 5432
}

def transaction_1():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    conn.autocommit = False

    print("T1: Locking account 1")
    cur.execute("SELECT * FROM accounts WHERE id = 1 FOR UPDATE")
    time.sleep(2)

    print("T1: Locking account 2")
    cur.execute("SELECT * FROM accounts WHERE id = 2 FOR UPDATE")

    conn.commit()
    cur.close()
    conn.close()

def transaction_2():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    conn.autocommit = False

    print("T2: Locking account 2")
    cur.execute("SELECT * FROM accounts WHERE id = 2 FOR UPDATE")
    time.sleep(2)

    print("T2: Locking account 1")
    cur.execute("SELECT * FROM accounts WHERE id = 1 FOR UPDATE")

    conn.commit()
    cur.close()
    conn.close()

t1 = threading.Thread(target=transaction_1)
t2 = threading.Thread(target=transaction_2)

t1.start()
t2.start()

t1.join()
t2.join()
