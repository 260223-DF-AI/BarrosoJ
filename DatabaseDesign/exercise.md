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

