-- Active: 1773160131354@@127.0.0.1@5432@chinook_pg
-- Parking Lot*******
-- *                *
-- *                *
--- *****************

-- SETUP:
-- Connect to the server (Azure Data Studio / Database extension/psql)
-- Create a database (I recommend chinook_pg)
-- Execute the Chinook database (from the Chinook_pg.sql file) to create Chinook resources in your server (I recommend doing this from psql)

-- Comment can be done single line with --
-- Comment can be done multi line with /* */

/*
DQL - Data Query Language
Keywords:

SELECT - retrieve data, select the columns from the resulting set
FROM - the table(s) to retrieve data from
WHERE - a conditional filter of the data
GROUP BY - group the data based on one or more columns
HAVING - a conditional filter of the grouped data
ORDER BY - sort the data
*/

SELECT * FROM actor;
SELECT last_name FROM actor;
SELECT * FROM actor WHERE first_name = 'Morgan';
select * from actor where first_name = 'John';

-- BASIC CHALLENGES
-- List all customers (full name, customer id, and country) who are not in the USA
SELECT 
    first_name || ' ' || last_name AS full_name,
    customer_id,
    country
FROM customer
WHERE country <> 'USA';

-- List all customers from Brazil
SELECT *
FROM customer
WHERE country = 'Brazil';


-- List all sales agents
SELECT *
FROM employee
WHERE title = 'Sales Support Agent';


-- Retrieve a list of all countries in billing addresses on invoices
SELECT DISTINCT billing_country
FROM invoice;

-- count number of uniques
SELECT COUNT (DISTINCT billing_country)
FROM invoice;

-- Retrieve how many invoices there were in 2009, and what was the sales total for that year?
SELECT COUNT(*), SUM(total)
FROM invoice
WHERE EXTRACT(YEAR FROM invoice_date) = 2009;

-- query to verify (verifuery)
-- SELECT *
-- FROM invoice
-- WHERE EXTRACT(YEAR FROM invoice_date) = 2009;

-- (challenge: find the invoice count sales total for every year using one query)
SELECT EXTRACT(YEAR FROM invoice_date) AS year, SUM(total)
FROM invoice
GROUP BY EXTRACT(YEAR FROM invoice_date)
ORDER BY year;

SELECT COUNT(DISTINCT EXTRACT(YEAR FROM invoice_date))
FROM invoice;

-- how many line items were there for invoice #37
SELECT COUNT(*) AS total_line_items
FROM invoice_line
WHERE invoice_id = 37;


-- how many invoices per country? BillingCountry  # of invoices -

SELECT billing_country AS country, COUNT(*) as invoice_num
FROM invoice
GROUP BY country
ORDER BY invoice_num DESC;

-- Retrieve the total sales per country, ordered by the highest total sales first.
SELECT billing_country AS country, SUM(total) AS total_country_sales
FROM invoice
GROUP BY country
ORDER BY total_country_sales DESC;


-- JOINS CHALLENGES
-- Every Album by Artist
SELECT *
FROM album alb JOIN ARTIST art
ON alb.artist_id = art.artist_id
ORDER BY name;


-- (inner keyword is optional for inner join)
-- All songs of the rock genre
SELECT ge.name, tr.name
FROM track tr JOIN genre ge
ON tr.genre_id = ge.genre_id
WHERE ge.name = 'Rock'
ORDER BY ge.name;


-- Show all invoices of customers from brazil (mailing address not billing)
SELECT *
FROM invoice i JOIN customer c
ON i.customer_id = c.customer_id
WHERE c.country = 'Brazil'
ORDER BY c.customer_id;


-- Show all invoices together with the name of the sales agent for each one
SELECT i.*, e.first_name || ' ' || e.last_name AS agent_name
FROM invoice i
    JOIN customer c ON i.customer_id = c.customer_id
    JOIN employee e ON e.employee_id = c.support_rep_id;

-- Which sales agent made the most sales in 2009?
SELECT e.first_name
FROM invoice i
    JOIN customer c ON i.customer_id = c.customer_id
    JOIN employee e ON e.employee_id = c.support_rep_id
WHERE EXTRACT(YEAR FROM i.invoice_date) = 2009
GROUP BY e.employee_id
LIMIT 1;

-- How many customers are assigned to each sales agent?
SELECT COUNT(support_rep_id) AS num_customers
FROM customer
GROUP BY support_rep_id
ORDER BY num_customers DESC;

-- Which track was purchased the most in 2010?
SELECT track.name, SUM(invoice_line.quantity) AS total_sold
    FROM track
    JOIN invoice_line on track.track_id = invoice_line.track_id
    JOIN invoice ON invoice.invoice_id = invoice_line.invoice_id
    WHERE EXTRACT(YEAR FROM invoice.invoice_date) = 2010
    GROUP BY track.name
    ORDER BY SUM(invoice_line.quantity) DESC, track.name ASC
    LIMIT 1;


SELECT COUNT(track_id) as total, il.track_id 
    FROM invoice_line il 
        JOIN invoice inv
    ON il.invoice_id = inv.invoice_id
    WHERE EXTRACT(YEAR FROM inv.invoice_date) = 2010
    GROUP BY il.track_id

SELECT * FROM invoice_line
WHERE quantity > 1;

SELECT track_id, COUNT(track_id) AS total
FROM invoice_line
GROUP BY track_id
ORDER BY total DESC; 

-- Show the top three best selling artists.


-- Which customers have the same initials as at least one other customer?


-- Which countries have the most invoices?


-- Which city has the customer with the highest sales total?


-- Who is the highest spending customer?


-- Return the email and full name of of all customers who listen to Rock.


-- Which artist has written the most Rock songs?


-- Which artist has generated the most revenue?




-- ADVANCED CHALLENGES
-- solve these with a mixture of joins, subqueries, CTE, and set operators.
-- solve at least one of them in two different ways, and see if the execution
-- plan for them is the same, or different.

-- 1. which artists did not make any albums at all?


-- 2. which artists did not record any tracks of the Latin genre?


-- 3. which video track has the longest length? (use media type table)


-- 4. boss employee (the one who reports to nobody)
SELECT 'Boss ' || first_name || ' ' || last_name big_boss_name
FROM employee
WHERE reports_to IS NULL;

-- 5. how many audio tracks were bought by German customers, and what was
--    the total price paid for them?
SELECT COUNT(*)
FROM customer

SELECT tr.id
FROM track tr
JOIN media_type mt
ON tr.media_type_id = mt.media_type_id
WHERE mt.name LIKE '%audio';

-- 6. list the names and countries of the customers supported by an employee
--    who was hired younger than 35.


-- DML exercises

-- 1. insert two new records into the employee table.


-- 2. insert two new records into the tracks table.


-- 3. update customer Aaron Mitchell's name to Robert Walter


-- 4. delete one of the employees you inserted.


-- 5. delete customer Robert Walter.
