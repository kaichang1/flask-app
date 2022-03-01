from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_chankaih'
app.config['MYSQL_PASSWORD'] = '7658' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_chankaih'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    query = """
    SELECT book_id, author_name, publisher_name, title, year, cost, quantity
    FROM Books
    JOIN Authors ON Books.author_id = Authors.author_id
    JOIN Publishers ON Books.publisher_id = Publishers.publisher_id;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    books = cur.fetchall()

    query = "SELECT author_id, author_name FROM Authors;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    authors = cur.fetchall()

    query = "SELECT publisher_id, publisher_name FROM Publishers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    publishers = cur.fetchall()

    return render_template("books.html", books=books, authors=authors, publishers=publishers)

@app.route('/authors')
def authors():
    query = "SELECT * FROM Authors;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    authors = cur.fetchall()

    return render_template("authors.html", authors=authors)

@app.route('/publishers')
def publishers():
    query = "SELECT * FROM Publishers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    publishers = cur.fetchall()

    return render_template('publishers.html', publishers=publishers)

@app.route('/customers')
def customers():
    query = "SELECT * FROM Customers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    customers = cur.fetchall()

    return render_template('customers.html', customers=customers)

@app.route('/orders')
def orders():
    query = """
    SELECT order_id, first_name, last_name, email, date, total_cost
    FROM Orders
    JOIN Customers ON Orders.customer_id = Customers.customer_id;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    orders = cur.fetchall()

    query = "SELECT customer_id FROM Customers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    customers = cur.fetchall()

    return render_template('orders.html', orders=orders, customers=customers)

@app.route('/order-details')
def order_details():
    query = """
    SELECT order_details_id, order_id, title, publisher_name, Order_details.cost, Order_details.quantity
    FROM Order_details
    JOIN Books ON Order_details.book_id = Books.book_id
    JOIN Publishers ON Books.publisher_id = Publishers.publisher_id;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    order_details = cur.fetchall()

    query = "SELECT order_id FROM Orders;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    orders = cur.fetchall()

    query = "SELECT book_id, title FROM Books;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    books = cur.fetchall()

    return render_template('order-details.html', order_details=order_details, orders=orders, books=books)

# Listener

if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted
    app.run(port=9115, debug=True)
