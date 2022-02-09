from flask import Flask, render_template, request
import os

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers', methods=['POST', 'GET'])
def customers():
    return render_template('customers.html')

@app.route('/orders', methods=['POST', 'GET'])
def orders():
    return render_template('orders.html')

@app.route('/order-details', methods=['POST', 'GET'])
def order_details():
    return render_template('order-details.html')

@app.route('/books')
def books():
    return render_template("books.html")

@app.route('/authors')
def authors():
    return render_template("authors.html")

@app.route('/publishers')
def publishers():
    return render_template('publishers.html')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9111)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 
