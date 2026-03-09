## Tables & Attributes outlined in ERD 
### Relationship mappings:

Customers -> Orders
- One customer may have many orders
- An order must have one customer
- No junction table required

Customers -> Reviews
- One customer may have many reviews
- A review must have one customer
- No junction table required

Books -> Authors
- One book may have many authors
- An author may have many books
- Junction table Books_Author required for many to many

Books -> Reviews
- One book may have many reviews
- A review must have one book
- No junction table required

Books -> Orders
- One book may have many orders
- An order may have many books
- Junction table Book_Orders required for M:M

Publishers -> Books
- One publisher may have many books
- A book must have one publisher
- No junction table required

### Three create table statements
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    bio varchar(500)
);

CREATE TABLE publishers (
    id SERIAL PRIMARY KEY,
    pub_name varchar(100),
    contact_info varchar(100)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    cust_id REFERENCES customers(id),
    status varchar(50)
);