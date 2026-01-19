'''
SELECT usename,pid,application_name,query,state
FROM pg_stat_activity
where datid is not NULL;

SELECT
  datname,
  datconnlimit
FROM pg_database
WHERE datname = 'postgres';

ALTER DATABASE postgres CONNECTION LIMIT 3;

select * from employees;

CREATE USER scofield
WITH PASSWORD 'scofield';

GRANT SELECT ON TABLE employees TO scofield;

'''


import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="scofield",
    password="scofield",
    host="localhost",
    application_name="fromPython",
    port=5432,
)

conn.set_session(autocommit=True)
cur = conn.cursor()

try:
    cur.execute("SELECT * FROM employees;")
    rows = cur.fetchall()
    
    for row in rows:
        print(row)

except Exception as e:
    print("Error while executing queries:", e) 
