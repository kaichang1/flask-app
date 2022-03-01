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
    query = "SELECT * FROM Books;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    books = cur.fetchall()

    query = "SELECT author_name FROM Authors;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    authors = cur.fetchall()

    query = "SELECT publisher_name FROM Publishers;"
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
    query = "SELECT * FROM Orders;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    orders = cur.fetchall()

    query = "SELECT first_name, last_name FROM Customers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    customers = cur.fetchall()

    return render_template('orders.html', orders=orders, customers=customers)

@app.route('/order-details')
def order_details():
    query = "SELECT * FROM Order_details;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    order_details = cur.fetchall()

    query = "SELECT order_id FROM Orders;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    orders = cur.fetchall()

    query = "SELECT title FROM Books;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    books = cur.fetchall()

    return render_template('order-details.html', order_details=order_details, orders=orders, books=books)

# Listener

if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted
    app.run(port=9115, debug=True)
