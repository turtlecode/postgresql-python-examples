'''
payroll_db :

CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC
);

INSERT INTO employees (full_name, department, salary) VALUES 
('Alice Smith', 'Engineering', 95000),
('Bob Johnson', 'Finance', 80000),
('Charlie Brown', 'HR', 72000);

select * from employees;

INSERT INTO employees (full_name, department, salary) 
VALUES ('Eve Taylor', 'Marketing', 58000);

#############################################################################

hr_db :

select * from employees;

CREATE EXTENSION postgres_fdw;

CREATE SERVER payroll_link
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host '127.0.0.1', port '5434', dbname 'payroll_db');

CREATE USER MAPPING FOR postgres
SERVER payroll_link
OPTIONS (user 'postgres', password 'turtlecode');

CREATE FOREIGN TABLE remote_employees (
    full_name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC
)
SERVER payroll_link
OPTIONS (table_name 'employees');

SELECT * FROM remote_employees;

INSERT INTO remote_employees (full_name, department, salary) 
VALUES ('David Miller', 'Sales', 65000);


'''

import psycopg2

# Configuration for HR Cluster (The Consumer)
DB_CONFIG = {
    "dbname": "hr_db",
    "user": "postgres",
    "password": "turtlecode",
    "host": "127.0.0.1",
    "port": "5433"
}

def main():
    try:
        print("--- ACCESSING HR SYSTEM (PORT 5433) ---")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Querying the foreign table (The bridge to Payroll)
        query = "SELECT full_name, salary FROM remote_employees;"
        cur.execute(query)

        print("Remote data fetched from Payroll via FDW:")
        for row in cur.fetchall():
            print(f"Name: {row[0]:<15} | Salary: {row[1]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    main()


#################################################################################


import psycopg2

# Configuration for Payroll Cluster (The Source)
DB_CONFIG = {
    "dbname": "payroll_db",
    "user": "postgres",
    "password": "your_password",
    "host": "127.0.0.1",
    "port": "5434"
}

def main():
    try:
        print("--- ACCESSING PAYROLL SYSTEM (PORT 5434) ---")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Querying the local physical table
        query = "SELECT emp_id, full_name, department FROM employees;"
        cur.execute(query)

        print("Local physical data in Payroll system:")
        for row in cur.fetchall():
            print(f"ID: {row[0]} | Name: {row[1]:<15} | Dept: {row[2]}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    main()
