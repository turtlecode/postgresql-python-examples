'''
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC
);

INSERT INTO products (name, price) VALUES
('Laptop', 1200),
('Phone', 800),
('Headphones', 150);

select * from products;

CREATE OR REPLACE FUNCTION get_discounted_price(product_id INT, discount_percent NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    original_price NUMERIC;
BEGIN

    SELECT price INTO original_price
    FROM products
    WHERE id = product_id;

    RETURN original_price * (1 - discount_percent / 100);
END;
$$ LANGUAGE plpgsql;


SELECT get_discounted_price(1, 10);
SELECT get_discounted_price(2, 10);
SELECT get_discounted_price(3, 10);

'''



import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="turtlecode",
    port="5432"
)

product_id = 2
discount_percent = 20

try:
    cur = conn.cursor()

    cur.execute(
        "SELECT get_discounted_price(%s, %s);",
        (product_id, discount_percent)
    )

    result = cur.fetchone()
    print(f"Discounted price: {int(result[0])}")

finally:
    cur.close()
    conn.close()
