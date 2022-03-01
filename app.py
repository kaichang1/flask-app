from flask import Flask, render_template, request
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    query = "SELECT * FROM Books;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()

    print(rows)

    query = "SELECT author_name FROM Authors;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    authors = db.execute_query(db_connection, query).fetchall()
    authors = tuple(sorted(authors))

    query = "SELECT publisher_name FROM Publishers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    publishers = db.execute_query(db_connection, query).fetchall()
    publishers = tuple(sorted(publishers))

    return render_template("books.html", rows=rows, authors=authors, publishers=publishers)

@app.route('/authors')
def authors():
    query = "SELECT * FROM Authors;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()
    return render_template("authors.html", rows=rows)

@app.route('/publishers')
def publishers():
    query = "SELECT * FROM Publishers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()
    return render_template('publishers.html', rows=rows)

@app.route('/customers')
def customers():
    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()
    return render_template('customers.html', rows=rows)

@app.route('/orders')
def orders():
    query = "SELECT * FROM Orders;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()

    query = "SELECT first_name, last_name FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    customers = db.execute_query(db_connection, query).fetchall()
    customers = tuple(sorted(customers))

    return render_template('orders.html', rows=rows, customers=customers)

@app.route('/order-details')
def order_details():
    query = "SELECT * FROM Order_details;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    rows = db.execute_query(db_connection, query).fetchall()

    query = "SELECT title FROM Books;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    books = db.execute_query(db_connection, query).fetchall()
    books = tuple(sorted(books))

    return render_template('order-details.html', rows=rows, books=books)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9115)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 
