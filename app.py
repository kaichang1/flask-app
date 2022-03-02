from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_chankaih'
app.config['MYSQL_PASSWORD'] = '7658'  # Last 4 of onid
app.config['MYSQL_DB'] = 'cs340_chankaih'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=["POST", "GET"])
def books():
    if request.method == "POST":
        if request.form.get("add_book"):
            author_id = request.form["author_id"]
            publisher_id = request.form["publisher_id"]
            title = request.form["title"]
            year = request.form["year"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            query = "INSERT INTO Books (author_id, publisher_id, title, year, cost, quantity) VALUES (%s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (author_id, publisher_id, title, year, cost, quantity))
            mysql.connection.commit()

        return redirect("/books")

    if request.method == "GET":
        query1 = """
            SELECT book_id, author_name, publisher_name, title, year, cost, quantity
            FROM Books
            JOIN Authors ON Books.author_id = Authors.author_id
            JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
            ORDER BY book_id;
            """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        books = cur.fetchall()

        query2 = "SELECT author_id, author_name FROM Authors;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        authors = cur.fetchall()

        query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        publishers = cur.fetchall()

        return render_template("books.html", books=books, authors=authors, publishers=publishers)

@app.route('/authors', methods=["POST", "GET"])
def authors():
    if request.method == "POST":
        if request.form.get("add_author"):
            author_name = request.form["author_name"]

            query = "INSERT INTO Authors (author_name) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (author_name,))
            mysql.connection.commit()

        return redirect("/authors")
        
    if request.method == "GET":
        query = "SELECT * FROM Authors;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        authors = cur.fetchall()

        return render_template("authors.html", authors=authors)

@app.route('/publishers', methods=["POST", "GET"])
def publishers():
    if request.method == "POST":
        if request.form.get("add_publisher"):
            publisher_name = request.form["publisher_name"]

            query = "INSERT INTO Publishers (publisher_name) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (publisher_name,))
            mysql.connection.commit()

        return redirect("/publishers")
        
    if request.method == "GET":
        query = "SELECT * FROM Publishers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        publishers = cur.fetchall()

        return render_template('publishers.html', publishers=publishers)

@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "POST":
        if request.form.get("add_customer"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            street = request.form["street"]
            city = request.form["city"]
            zip = request.form["zip"]

            query = "INSERT INTO Customers (first_name, last_name, email, phone, street, city, zip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, email, phone, street, city, zip))
            mysql.connection.commit()

        return redirect("/customers")
    if request.method == "GET":
        query = "SELECT * FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        customers = cur.fetchall()

        return render_template('customers.html', customers=customers)

@app.route('/orders', methods=["POST", "GET"])
def orders():
    if request.method == "POST":
        if request.form.get("add_order"):
            customer_id = request.form["customer_id"]
            date = request.form["date"]
            total_cost = request.form["total_cost"]
            
            query = "INSERT INTO Orders (customer_id, date, total_cost) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id, date, total_cost))
            mysql.connection.commit()

        return redirect("/orders")

    if request.method == "GET":
        query = """
        SELECT order_id, first_name, last_name, email, date, total_cost
        FROM Orders
        JOIN Customers ON Orders.customer_id = Customers.customer_id
        ORDER BY order_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        orders = cur.fetchall()

        query1 = "SELECT customer_id FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        customers = cur.fetchall()

        return render_template('orders.html', orders=orders, customers=customers)

@app.route('/order-details', methods=["POST", "GET"])
def order_details():
    if request.method == "POST":
        if request.form.get("add_order_detail"):
            order_id = request.form["order_id"]
            book_id = request.form["book_id"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            query = "INSERT INTO Order_details (order_id, book_id, cost, quantity) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, book_id, cost, quantity))
            mysql.connection.commit()
        return redirect("/order-details")

    if request.method == "GET":
        query = """
        SELECT order_details_id, order_id, title, publisher_name, Order_details.cost, Order_details.quantity
        FROM Order_details
        JOIN Books ON Order_details.book_id = Books.book_id
        JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
        ORDER BY order_details_id;
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
    # Start the app on port 3000, it will be different once hosted
    app.run(port=9115, debug=True)
