-- For Books
-- get all books
SELECT book_id, author_name, publisher_name, title, year, cost, quantity
  FROM Books
  JOIN Authors ON Books.author_id = Authors.author_id
  LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
  ORDER BY book_id;
-- get all info about a book based on the user input in search area
SELECT book_id, author_name, publisher_name, title, year, cost, quantity
  FROM Books
  JOIN Authors ON Books.author_id = Authors.author_id
  LEFT JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
  WHERE title = :title AND author_name = :author_name
  ORDER BY book_id;
-- add new book
INSERT INTO Books (author_id, publisher_id, title, year, cost, quantity)
VALUES (:author_id, :publisher_id, :title, :year, :cost, :quantity);
-- update a specific row that the user chose, based on the primary key value (entity id)
UPDATE Books
SET author_id = :author_id, publisher_id = :publisher_id, title = :title, year = :year, cost = :cost, quantity = :quantity
WHERE book_id = :book_id;
-- delete a specific row that the user chose, based on the primary key value (entity id)
DELETE FROM Books WHERE book_id = :book_id;


-- For Authors
-- get all authors
SELECT * FROM Authors;
-- get all info about an author based on the user input in search area
SELECT * FROM Authors WHERE author_name = :author_name;
-- add new author
INSERT INTO Authors (author_name)
VALUES (:author_name);
-- update a specific row that the user chose, based on the primary key value (entity id)
UPDATE Authors
SET author_name = :author_name
WHERE author_id = :author_id;
-- delete a specific row that the user chose, based on the primary key value (entity id)
DELETE FROM Authors WHERE author_id = :author_id;


-- For Publishers
-- get all publishers
SELECT * FROM Publishers;
-- get all info about an publisher based on the user input in search area
SELECT * FROM Publishers WHERE publisher_name = :publisher_name;
-- add new publisher
INSERT INTO Publishers (publisher_name)
VALUES (:publisher_name);
-- update a specifc row that the user chose, based on the entity id
UPDATE Publishers
SET publisher_name = :publisher_name
WHERE publisher_id = :publisher_id;
-- delete a specific row that the user chose, based on the entity id
DELETE FROM Publishers WHERE publisher_id = :publisher_id;


-- For Customers
-- get all customers
SELECT * FROM Customers;
-- add new customer
INSERT INTO Customers (first_name, last_name, email, phone, street, city, zip)
VALUES (:first_name, :last_name, :email, :phone, :street, :city, :zip);
-- update a specific row that the user chose, based on the entity id
UPDATE Customers
SET first_name = :first_name, last_name = :last_name, email = :email, phone = :phone, street = :street, city = :city, zip = :zip
WHERE customer_id = :customer_id;
-- delete a specific row that the user chose, based on the entity id
DELETE FROM Customers WHERE customer_id = :customer_id;


-- For Orders
-- get all orders
SELECT order_id, first_name, last_name, email, date, total_cost
  FROM Orders
  JOIN Customers ON Orders.customer_id = Customers.customer_id
  ORDER BY order_id;
-- add new order
INSERT INTO Orders (customer_id, date, total_cost)
VALUES (:customer_id, :date, :total_cost);
-- update a specific row that the user chose, based on the entity id
UPDATE Orders
SET customer_id = :customer_id, date = :date, total_cost = :total_cost
WHERE order_id = :order_id;
-- delete a specific row that the user chose, based on the entity id
DELETE FROM Orders WHERE order_id = :order_id;


-- For Order_details
-- get all order details
SELECT order_details_id, order_id, title, publisher_name, Order_details.cost, Order_details.quantity
  FROM Order_details
  JOIN Books ON Order_details.book_id = Books.book_id
  JOIN Publishers ON Books.publisher_id = Publishers.publisher_id
  ORDER BY order_details_id;
-- add new order detail
INSERT INTO Order_details (order_id, book_id, cost, quantity)
VALUES (:order_id, :book_id, :cost, :quantity);
-- update a specifc row that the user chose, based on the entity id
UPDATE Order_details
SET order_id = :order_id, book_id = :book_id, cost = :cost, quantity = :quantity
WHERE order_detail_id = :order_detail_id;
-- delete a specific row that the user chose, based on the entity id
DELETE FROM Order_details WHERE order_detail_id = :order_detail_id;
