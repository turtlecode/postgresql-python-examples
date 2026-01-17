'''
CREATE USER scofield WITH PASSWORD 'scofield';

CREATE SCHEMA IF NOT EXISTS scofield AUTHORIZATION scofield;

CREATE TABLESPACE scofield_ts
OWNER scofield
LOCATION 'D:\tablespaces';

CREATE TABLE scofield.orders (
    id SERIAL,
    order_date DATE NOT NULL,
    amount NUMERIC
)
PARTITION BY RANGE (order_date)
TABLESPACE scofield_ts;

CREATE TABLE scofield.orders_2024
PARTITION OF scofield.orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
TABLESPACE scofield_ts;

CREATE TABLE scofield.orders_2025
PARTITION OF scofield.orders
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01')
TABLESPACE scofield_ts;

GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA scofield TO scofield;
GRANT USAGE, SELECT ON SEQUENCE scofield.orders_id_seq TO scofield;

'''
#insert

import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="scofield",
    password="scofield",
    host="localhost",
    port=5432
)

conn.set_session(autocommit=True)
cur = conn.cursor()

try:
    cur.execute("""
    INSERT INTO scofield.orders (order_date, amount)
    VALUES
        ('2024-06-15', 100.50),
        ('2025-02-10', 250.75);
    """)

    inserted_rows = cur.rowcount

    if inserted_rows > 0:
        print(f"Insert successful. {inserted_rows} rows inserted.")
    else:
        print("Insert executed but no rows were inserted.")

except Exception as e:
    print("Insert failed:", e)

#select

import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="scofield",
    password="scofield",
    host="localhost",
    port=5432
)

conn.set_session(autocommit=True)
cur = conn.cursor()


queries = [
    ("orders", "SELECT * FROM scofield.orders;"),
    ("orders_2024", "SELECT * FROM scofield.orders_2024;"),
    ("orders_2025", "SELECT * FROM scofield.orders_2025;")
]

try:
    for label, sql in queries:
        print(f"\nRunning query: {label}")
        cur.execute(sql)

        rows = cur.fetchall()

        if rows:
            print(f"{len(rows)} row(s) found:")
            for row in rows:
                print(row)
        else:
            print("No rows found.")

except Exception as e:
    print("Error while executing queries:", e)
