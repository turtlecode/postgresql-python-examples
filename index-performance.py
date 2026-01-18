'''
create table EMPLOYEES (
	id INT,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50),
	gender VARCHAR(50),
	salary INT
);

INSERT INTO employees (id, first_name, last_name, email, gender, salary)
SELECT
    gs,
    'First'||gs,
    'Last'||gs,
    'email'||gs||'@example.com',
    CASE WHEN gs%2=0 THEN 'M' ELSE 'F' END,
    (gs%10000)+3000
FROM generate_series(1,10000000) gs;

select count(*) from employees;

CREATE INDEX idx_employees_salary
ON employees(salary);

DROP INDEX idx_employees_salary;

'''

import psycopg2
import time

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="turtlecode"
)

cur = conn.cursor()

# List of queries to test
queries = [
    "SELECT * FROM employees WHERE salary = 90000",
    "SELECT * FROM employees WHERE salary = 180000",
    "SELECT * FROM employees WHERE salary = 360000",
    "SELECT * FROM employees WHERE salary = 720000"
]

# Number of times to repeat each query for averaging
repeats = 5

def run_test():
    for query in queries:
        times = []
        for _ in range(repeats):
            start = time.time()
            cur.execute(query)
            cur.fetchall()  # Fetch all rows to measure real execution time
            end = time.time()
            times.append((end - start) * 1000)  # milliseconds
        avg_time = sum(times) / len(times)
        print(f"{query} -> Average time: {avg_time:.2f} ms")

# Run performance test
run_test()

cur.close()
conn.close()
