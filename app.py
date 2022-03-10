from flask import Flask, render_template, redirect, request, flash
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
# Necessary for flash
app.secret_key = 'not_so_secret_secret_key'

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_chankaih'
app.config['MYSQL_PASSWORD'] = '7658'  # Last 4 of ONID
app.config['MYSQL_DB'] = 'cs340_chankaih'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/books", methods=["POST", "GET"])
def books():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_book"):
            author_id = request.form["author_id"]
            publisher_id = request.form["publisher_id"]
            title = request.form["title"]
            year = request.form["year"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            try:
                # If publisher_id, year, and cost are all NULL
                if publisher_id == "0" and year == "" and cost == "":
                    query = "INSERT INTO Books (author_id, title, quantity) VALUES (%s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, quantity))
                    mysql.connection.commit()

                # If only publisher_id, year are NULL
                elif publisher_id == "0" and year == "":
                    query = "INSERT INTO Books (author_id, title, cost, quantity) VALUES (%s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, cost, quantity))
                    mysql.connection.commit()

                # If only publisher_id, cost are NULL
                elif publisher_id == "0" and cost == "":
                    query = "INSERT INTO Books (author_id, title, year, quantity) VALUES (%s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, year, quantity))
                    mysql.connection.commit()

                # If only year, cost are NULL
                elif year == "" and cost == "":
                    query = "INSERT INTO Books (author_id, publisher_id, title, quantity) VALUES (%s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, quantity))
                    mysql.connection.commit()
                    

                # If only publisher_id is NULL
                elif publisher_id == "0":
                    query = "INSERT INTO Books (author_id, title, year, cost, quantity) VALUES (%s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, year, cost, quantity))
                    mysql.connection.commit()

                # If only year is NULL
                elif year == "":
                    query = "INSERT INTO Books (author_id, publisher_id, title, cost, quantity) VALUES (%s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, cost, quantity))
                    mysql.connection.commit()

                # If only cost is NULL
                elif cost == "":
                    query = "INSERT INTO Books (author_id, publisher_id, title, year, quantity) VALUES (%s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, year, quantity))
                    mysql.connection.commit()

                # If no NULL inputs
                else:
                    query = "INSERT INTO Books (author_id, publisher_id, title, year, cost, quantity) VALUES (%s, %s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, year, cost, quantity))
                    mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/books")

    if request.method == "GET":
        # If user is performing a search
        if request.args.get("search_book"):
            title = request.args["title"]
            author = request.args["author"]

            title = '%' + title + '%'
            author = '%' + author + '%'

            # If title is NULL
            if title == "":
                query1 = """
                    SELECT book_id, author_name, publisher_name, title, year, cost, quantity
                    FROM Books
                    JOIN Authors ON Books.author_id = Authors.author_id
                    LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
                    WHERE author_name LIKE (%s)
                    ORDER BY book_id;
                    """
                cur = mysql.connection.cursor()
                cur.execute(query1, (author,))
                books = cur.fetchall()

                query2 = "SELECT author_id, author_name FROM Authors;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                authors = cur.fetchall()

                query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                publishers = cur.fetchall()

            # If author is NULL
            elif author == "":
                query1 = """
                    SELECT book_id, author_name, publisher_name, title, year, cost, quantity
                    FROM Books
                    JOIN Authors ON Books.author_id = Authors.author_id
                    LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
                    WHERE title LIKE (%s)
                    ORDER BY book_id;
                    """
                cur = mysql.connection.cursor()
                cur.execute(query1, (title,))
                books = cur.fetchall()

                query2 = "SELECT author_id, author_name FROM Authors;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                authors = cur.fetchall()

                query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                publishers = cur.fetchall()

            # If no NULL inputs
            else:
                query1 = """
                    SELECT book_id, author_name, publisher_name, title, year, cost, quantity
                    FROM Books
                    JOIN Authors ON Books.author_id = Authors.author_id
                    LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
                    WHERE title LIKE (%s) AND author_name LIKE (%s)
                    ORDER BY book_id;
                    """
                cur = mysql.connection.cursor()
                cur.execute(query1, (title, author))
                books = cur.fetchall()

                query2 = "SELECT author_id, author_name FROM Authors;"
                cur = mysql.connection.cursor()
                cur.execute(query2)
                authors = cur.fetchall()

                query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
                cur = mysql.connection.cursor()
                cur.execute(query3)
                publishers = cur.fetchall()
            
            if not books:
                books = ({"book_id": "", "author_name": "", "publisher_name": "", "title": "", "year": "", "cost": "", "quantity": ""},)

        # Normal page load
        else:
            query1 = """
                SELECT book_id, author_name, publisher_name, title, year, cost, quantity
                FROM Books
                JOIN Authors ON Books.author_id = Authors.author_id
                LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
                ORDER BY book_id;
                """
            cur = mysql.connection.cursor()
            cur.execute(query1)
            books = cur.fetchall()

            query2 = "SELECT author_id, author_name FROM Authors;"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            authors = cur.fetchall()
            authors = sorted(authors, key=lambda item: item['author_name'])

            query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
            cur = mysql.connection.cursor()
            cur.execute(query3)
            publishers = cur.fetchall()
            publishers = sorted(publishers, key=lambda item: item['publisher_name'])

        return render_template("books.html", books=books, authors=authors, publishers=publishers)

# Delete functionality for books page.
@app.route("/delete-books/<int:id>")
def delete_books(id):
    query = "DELETE FROM Books WHERE book_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/books")

# If user attempts to delete an empty row (from an empty search)
@app.route("/delete-books/")
def delete_books_empty():
    return redirect("/books")

# Update functionality for books page
@app.route("/update-books/<int:id>", methods=["POST", "GET"])
def update_books(id):
    # User selected an entry to update
    if request.method == "GET":
        query1 = """
            SELECT book_id, author_name, publisher_name, title, year, cost, quantity
            FROM Books
            JOIN Authors ON Books.author_id = Authors.author_id
            LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
            WHERE book_id = (%s)
            ORDER BY book_id;
            """
        cur = mysql.connection.cursor()
        cur.execute(query1, (id,))
        # A tuple of one book, represented as a dictionary
        books = cur.fetchall()

        query2 = "SELECT author_id, author_name FROM Authors;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        authors = cur.fetchall()
        authors = sorted(authors, key=lambda item: item['author_name'])

        query3 = "SELECT publisher_id, publisher_name FROM Publishers;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        publishers = cur.fetchall()
        publishers = sorted(publishers, key=lambda item: item['publisher_name'])

        return render_template("update-books.html", books=books, authors=authors, publishers=publishers)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_book"):
            author_id = request.form["author_id"]
            publisher_id = request.form["publisher_id"]
            title = request.form["title"]
            year = request.form["year"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            try:
                # If publisher_id, year, and cost are all NULL
                if publisher_id == "0" and year == "" and cost == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = NULL, title = (%s), year = NULL, cost = NULL, quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, quantity, id))
                    mysql.connection.commit()

                # If only publisher_id, year are NULL
                elif publisher_id == "0" and year == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = NULL, title = (%s), year = NULL, cost = (%s), quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, cost, quantity, id))
                    mysql.connection.commit()

                # If only publisher_id, cost are NULL
                elif publisher_id == "0" and cost == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = NULL, title = (%s), year = (%s), cost = NULL, quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, year, quantity, id))
                    mysql.connection.commit()

                # If only year, cost are NULL
                elif year == "" and cost == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = (%s), title = (%s), year = NULL, cost = NULL, quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, quantity, id))
                    mysql.connection.commit()

                # If only publisher_id is NULL
                elif publisher_id == "0":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = NULL, title = (%s), year = (%s), cost = (%s), quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, title, year, cost, quantity, id))
                    mysql.connection.commit()

                # If only year is NULL
                elif year == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = (%s), title = (%s), year = NULL, cost = (%s), quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, cost, quantity, id))
                    mysql.connection.commit()

                # If only cost is NULL
                elif cost == "":
                    query = "UPDATE Books SET author_id = (%s), publisher_id = (%s), title = (%s), year = (%s), cost = NULL, quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, year, quantity, id))
                    mysql.connection.commit()

                # If no NULL inputs
                else:
                    query = "UPDATE Books SET author_id = (%s), publisher_id = (%s), title = (%s), year = (%s), cost = (%s), quantity = (%s) WHERE book_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (author_id, publisher_id, title, year, cost, quantity, id))
                    mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/books")

# If user attempts to delete an empty row (from an empty search)
@app.route("/update-books/")
def update_books_empty():
    return redirect("/books")

@app.route("/authors", methods=["POST", "GET"])
def authors():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_author"):
            author_name = request.form["author_name"]

            try:
                query = "INSERT INTO Authors (author_name) VALUES (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (author_name,))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/authors")
        
    if request.method == "GET":
        # If user is performing a search
        if request.args.get("search_author"):
            author_name = request.args["author_name"]
            author_name = '%' + author_name + '%'

            query = "SELECT * FROM Authors WHERE author_name LIKE (%s) ORDER BY author_id;"
            cur = mysql.connection.cursor()
            cur.execute(query, (author_name,))
            authors = cur.fetchall()

            if not authors:
                authors = ({"author_id": "", "author_name": ""},)

        # Normal page load
        else:
            query = "SELECT * FROM Authors ORDER BY author_id;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            authors = cur.fetchall()

        return render_template("authors.html", authors=authors)

# Delete functionality for authors page.
@app.route("/delete-authors/<int:id>")
def delete_authors(id):
    query = "DELETE FROM Authors WHERE author_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/authors")

# If user attempts to delete an empty row (from an empty search)
@app.route("/delete-authors/")
def delete_authors_empty():
    return redirect("/authors")

# Update functionality for authors page
@app.route("/update-authors/<int:id>", methods=["POST", "GET"])
def update_authors(id):
    # User selected an entry to update
    if request.method == "GET":
        query = "SELECT * FROM Authors WHERE author_id = (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        # A tuple of one author, represented as a dictionary
        authors = cur.fetchall()

        return render_template("update-authors.html", authors=authors)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_author"):
            author_name = request.form["author_name"]

            try:
                query = "UPDATE Authors SET author_name = (%s) WHERE author_id = (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (author_name, id))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/authors")

# If user attempts to delete an empty row (from an empty search)
@app.route("/update-authors/")
def update_authors_empty():
    return redirect("/authors")

@app.route("/publishers", methods=["POST", "GET"])
def publishers():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_publisher"):
            publisher_name = request.form["publisher_name"]

            try:
                query = "INSERT INTO Publishers (publisher_name) VALUES (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (publisher_name,))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/publishers")
        
    if request.method == "GET":
        # If user is performing a search
        if request.args.get("search_publisher"):
            publisher_name = request.args["publisher_name"]
            publisher_name = '%' + publisher_name + '%'

            query = "SELECT * FROM Publishers WHERE publisher_name LIKE (%s) ORDER BY publisher_id;"
            cur = mysql.connection.cursor()
            cur.execute(query, (publisher_name,))
            publishers = cur.fetchall()

            if not publishers:
                publishers = ({"publisher_id": "", "publisher_name": ""},)

        # Normal page load
        else:
            query = "SELECT * FROM Publishers ORDER BY publisher_id;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            publishers = cur.fetchall()

        return render_template('publishers.html', publishers=publishers)

# Delete functionality for publishers page.
@app.route("/delete-publishers/<int:id>")
def delete_publishers(id):
    query = "DELETE FROM Publishers WHERE publisher_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/publishers")

# If user attempts to delete an empty row (from an empty search)
@app.route("/delete-publishers/")
def delete_publishers_empty():
    return redirect("/publishers")

# Update functionality for publishers page
@app.route("/update-publishers/<int:id>", methods=["POST", "GET"])
def update_publishers(id):
    # User selected an entry to update
    if request.method == "GET":
        query = "SELECT * FROM Publishers WHERE publisher_id = (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        # A tuple of one publisher, represented as a dictionary
        publishers = cur.fetchall()

        return render_template("update-publishers.html", publishers=publishers)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_publisher"):
            publisher_name = request.form["publisher_name"]

            try:
                query = "UPDATE Publishers SET publisher_name = (%s) WHERE publisher_id = (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (publisher_name, id))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/publishers")

# If user attempts to delete an empty row (from an empty search)
@app.route("/update-publishers/")
def update_publishers_empty():
    return redirect("/publishers")

@app.route("/customers", methods=["POST", "GET"])
def customers():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_customer"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            street = request.form["street"]
            city = request.form["city"]
            zip = request.form["zip"]

            try:
                # If phone is NULL
                if phone == "":
                    query = "INSERT INTO Customers (first_name, last_name, email, street, city, zip) VALUES (%s, %s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (first_name, last_name, email, street, city, zip))
                    mysql.connection.commit()

                # If no NULL inputs
                else:
                    query = "INSERT INTO Customers (first_name, last_name, email, phone, street, city, zip) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (first_name, last_name, email, phone, street, city, zip))
                    mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/customers")

    # Normal page load
    if request.method == "GET":
        query = "SELECT * FROM Customers ORDER BY customer_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        customers = cur.fetchall()

        return render_template('customers.html', customers=customers)

# Delete functionality for customers page.
@app.route("/delete-customers/<int:id>")
def delete_customers(id):
    query = "DELETE FROM Customers WHERE customer_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/customers")

# Update functionality for customers page
@app.route("/update-customers/<int:id>", methods=["POST", "GET"])
def update_customers(id):
    # User selected an entry to update
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = (%s) ORDER BY customer_id;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        # A tuple of one customer, represented as a dictionary
        customers = cur.fetchall()

        return render_template('update-customers.html', customers=customers)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_customer"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            street = request.form["street"]
            city = request.form["city"]
            zip = request.form["zip"]

            try:
                # If phone is NULL
                if phone == "":
                    query = "UPDATE Customers SET first_name = (%s), last_name = (%s), email = (%s), phone = NULL, street = (%s), city = (%s), zip = (%s) WHERE customer_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (first_name, last_name, email, street, city, zip, id))
                    mysql.connection.commit()

                # If no NULL inputs
                else:
                    query = "UPDATE Customers SET first_name = (%s), last_name = (%s), email = (%s), phone = (%s), street = (%s), city = (%s), zip = (%s) WHERE customer_id = (%s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (first_name, last_name, email, phone, street, city, zip, id))
                    mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/customers")

@app.route("/orders", methods=["POST", "GET"])
def orders():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_order"):
            customer_id = request.form["customer_id"]
            date = request.form["date"]
            total_cost = request.form["total_cost"]
            
            try:
                query = "INSERT INTO Orders (customer_id, date, total_cost) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_id, date, total_cost))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/orders")

    # Normal page load
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
        customers = sorted(customers, key=lambda item: item['customer_id'])

        return render_template('orders.html', orders=orders, customers=customers)

# Delete functionality for orders page.
@app.route("/delete-orders/<int:id>")
def delete_orders(id):
    query = "DELETE FROM Orders WHERE order_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/orders")

# Update functionality for orders page
@app.route("/update-orders/<int:id>", methods=["POST", "GET"])
def update_orders(id):
    # User selected an entry to update
    if request.method == "GET":
        query = """
        SELECT order_id, first_name, last_name, email, date, total_cost
        FROM Orders
        JOIN Customers ON Orders.customer_id = Customers.customer_id
        WHERE order_id = (%s)
        ORDER BY order_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        # A tuple of one order, represented as a dictionary
        orders = cur.fetchall()

        query1 = "SELECT customer_id, email FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        customers = cur.fetchall()
        customers = sorted(customers, key=lambda item: item['customer_id'])

        return render_template('update-orders.html', orders=orders, customers=customers)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_order"):
            customer_id = request.form["customer_id"]
            date = request.form["date"]
            total_cost = request.form["total_cost"]
            
            try:
                query = "UPDATE Orders SET customer_id = (%s), date = (%s), total_cost = (%s) WHERE order_id = (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (customer_id, date, total_cost, id))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/orders")

@app.route("/order-details", methods=["POST", "GET"])
def order_details():
    # If user is adding a new entry
    if request.method == "POST":
        if request.form.get("add_order_detail"):
            order_id = request.form["order_id"]
            book_id = request.form["book_id"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            try:
                query = "INSERT INTO Order_details (order_id, book_id, cost, quantity) VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_id, book_id, cost, quantity))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")

        return redirect("/order-details")

    # Normal page load
    if request.method == "GET":
        query1 = """
        SELECT order_details_id, order_id, Books.book_id, title, author_name, publisher_name, Order_details.cost, Order_details.quantity
        FROM Order_details
        JOIN Books ON Order_details.book_id = Books.book_id
        JOIN Authors ON Books.author_id = Authors.author_id
        JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
        ORDER BY order_details_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query1)
        order_details = cur.fetchall()

        query2 = "SELECT order_id FROM Orders;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        orders = cur.fetchall()
        orders = sorted(orders, key=lambda item: item['order_id'])

        query3 = "SELECT book_id, title FROM Books;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        books = cur.fetchall()
        books = sorted(books, key=lambda item: item['book_id'])

        return render_template('order-details.html', order_details=order_details, orders=orders, books=books)

# Delete functionality for order-details page.
@app.route("/delete-order-details/<int:id>")
def delete_order_details(id):
    query = "DELETE FROM Order_details WHERE order_details_id = (%s);"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/order-details")

# Update functionality for order-details page
@app.route("/update-order-details/<int:id>", methods=["POST", "GET"])
def update_order_details(id):
    # User selected an entry to update
    if request.method == "GET":
        query1 = """
        SELECT order_details_id, order_id, Books.book_id, title, author_name, publisher_name, Order_details.cost, Order_details.quantity
        FROM Order_details
        JOIN Books ON Order_details.book_id = Books.book_id
        JOIN Authors ON Books.author_id = Authors.author_id
        JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
        WHERE order_details_id = (%s)
        ORDER BY order_details_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query1, (id,))
        # A tuple of one order-detail, represented as a dictionary
        order_details = cur.fetchall()

        query2 = "SELECT order_id FROM Orders;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        orders = cur.fetchall()
        orders = sorted(orders, key=lambda item: item['order_id'])

        query3 = "SELECT book_id, title, author_name, publisher_name FROM Books JOIN Authors ON Books.author_id = Authors.author_id JOIN Publishers ON Books.publisher_id = Publishers.publisher_id;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        books = cur.fetchall()
        books = sorted(books, key=lambda item: item['book_id'])

        return render_template('update-order-details.html', order_details=order_details, orders=orders, books=books)

    # User clicks "Update"
    if request.method == "POST":
        if request.form.get("update_order_detail"):
            order_id = request.form["order_id"]
            book_id = request.form["book_id"]
            cost = request.form["cost"]
            quantity = request.form["quantity"]

            try:
                query = "UPDATE Order_details SET order_id = (%s), book_id = (%s), cost = (%s), quantity = (%s) WHERE order_details_id = (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (order_id, book_id, cost, quantity, id))
                mysql.connection.commit()

            except MySQLdb._exceptions.IntegrityError:
                flash("Error: MySQL IntegrityError. You may be breaking UNIQUE constraints. Please try again.")
                return redirect("#")

        return redirect("/order-details")

# Listener

if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=9115, debug=True)
