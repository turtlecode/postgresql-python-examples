

""" PYTHON CODES (BELOW) & SQL CODES

CREATE TABLE customer_balance (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    balance NUMERIC(10, 2) NOT NULL
);

INSERT INTO customer_balance (customer_id, customer_name, balance)
VALUES
(1, 'Micheal Scofield', 1000.00),
(2, 'John Abruzzi', 1000.00);

SELECT * FROM customer_balance;

CALL transfer_money(2, 1, 1100.00);

----------------------------CREATE PROCEDURE-----------------------------


CREATE OR REPLACE PROCEDURE transfer_money(
    sender_id INT,
    receiver_id INT,
    transfer_amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check sender balance
    IF (SELECT balance FROM customer_balance WHERE customer_id = sender_id) < transfer_amount THEN
        RAISE EXCEPTION 'Insufficient balance for customer %', sender_id;
    END IF;

    -- Deduct money from sender
    UPDATE customer_balance
    SET balance = balance - transfer_amount
    WHERE customer_id = sender_id;

    -- Add money to receiver
    UPDATE customer_balance
    SET balance = balance + transfer_amount
    WHERE customer_id = receiver_id;

    COMMIT;
END;
$$;

"""

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="turtlecode",
    port="5432"
)
conn.autocommit = True


def transfer_money(sender_id, receiver_id, amount):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "CALL transfer_money(%s, %s, %s);",
            (sender_id, receiver_id, amount)
        )

        conn.commit()
        print("Transfer completed successfully")

    except Exception as e:
        conn.rollback()
        print("Transfer failed:", e)

    finally:
        cursor.close()


def get_balances():
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, customer_name,\
                    balance FROM customer_balance")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()

transfer_money(1, 2, 100.00)

get_balances()
