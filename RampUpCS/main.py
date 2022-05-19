import sqlite3
con = sqlite3.connect(r'ramp_up_demo_db.sqlite')
cur = con.cursor()
print('(a)')
for row in cur.execute('SELECT sales_name FROM Product ORDER BY price DESC LIMIT 1'):
        print(row)
for row in cur.execute('SELECT sales_name FROM Product WHERE price=(SELECT max(price) FROM Product)'):
        print(row)
print('(b)')
ids = []
for row in cur.execute(
    """
    WITH joined_table AS (
        SELECT * FROM Customer 
        JOIN Address 
        ON Customer.address == Address.aid
    ) 
    SELECT cust_id FROM joined_table WHERE city='Pittsfield' AND date_of_birth < '19891001'"""
):
    ids.append(row[0])
print(ids)

print('(c)')
for row in cur.execute(
    """
    WITH recipe_with_positions AS (
        SELECT * FROM ReceiptPositions AS pos
        JOIN SalesReceipt
        ON pos.rec_id == SalesReceipt.rec_id
    ), 
    positions_with_producut_name AS (
        SELECT * FROM recipe_with_positions
        JOIN Product
        ON product == Product.prod_id
    ) 
    SELECT rec_id, SUM(quantity) AS count 
    FROM positions_with_producut_name 
    WHERE sales_name IN ('W', 'Y', 'Z') 
    GROUP BY rec_id 
    ORDER BY count DESC
    LIMIT 1"""
):
    print(row)

print('(d)')
for row in cur.execute(
    """
    WITH joined_table AS (
        SELECT * FROM Stock 
        JOIN Product 
        ON Stock.product == Product.prod_id
    )
    SELECT store FROM joined_table WHERE sales_name == 'X' AND current_stock < 1.2 * safety_stock"""
):
    print(row)

print('(e)')
for row in cur.execute(
    """
    WITH recipe_with_positions AS (
        SELECT * FROM SalesReceipt
        JOIN ReceiptPositions 
        ON SalesReceipt.rec_id == ReceiptPositions.rec_id
        WHERE date BETWEEN '20210101' AND '20211231'
    ), 
    positions_with_product AS (
        SELECT * FROM recipe_with_positions
        JOIN Product 
        ON recipe_with_positions.product == Product.prod_id
    ),
    positions_with_store AS (
        SELECT * FROM positions_with_product
        JOIN Salesperson 
        ON positions_with_product.salesperson == Salesperson.sid
        JOIN Store
        ON works_in == Store.store_id
    ),
    revenue_per_director_with_name AS (
        SELECT * FROM (
            SELECT director, SUM(price * quantity) AS revenue 
            FROM positions_with_store
            GROUP BY director
        )
        JOIN Salesperson
        ON director == Salesperson.sid
    )
    SELECT first_name, last_name FROM revenue_per_director_with_name WHERE revenue=(SELECT max(revenue) FROM revenue_per_director_with_name)
    """
):
    print(row)

# Check, if groupby worked
# for row in cur.execute(
#     """
#     SELECT * FROM ReceiptPositions 
#     JOIN Product
#     ON product == Product.prod_id
#     WHERE rec_id == 825
#     """
# ):
#     print(row)