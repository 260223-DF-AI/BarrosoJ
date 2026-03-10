-- -- Active: 1773160131354@@127.0.0.1@5432@sql_practice
-- -- CREATE DATABASE sql_practice;

-- -- Create tables
-- CREATE TABLE departments (
--     dept_id SERIAL PRIMARY KEY,
--     dept_name VARCHAR(50) NOT NULL,
--     location VARCHAR(100),
--     budget DECIMAL(12, 2)
-- );

-- CREATE TABLE employees (
--     emp_id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     email VARCHAR(100) UNIQUE,
--     hire_date DATE DEFAULT CURRENT_DATE,
--     salary DECIMAL(10, 2),
--     dept_id INTEGER REFERENCES departments(dept_id)
-- );

-- CREATE TABLE projects (
--     project_id SERIAL PRIMARY KEY,
--     project_name VARCHAR(100) NOT NULL,
--     start_date DATE,
--     end_date DATE,
--     budget DECIMAL(12, 2),
--     dept_id INTEGER REFERENCES departments(dept_id)
-- );

-- -- Insert sample data
-- INSERT INTO departments (dept_name, location, budget) VALUES
-- ('Engineering', 'Building A', 500000),
-- ('Sales', 'Building B', 300000),
-- ('Marketing', 'Building C', 200000),
-- ('HR', 'Building D', 150000);

-- INSERT INTO employees (first_name, last_name, email, hire_date, salary, dept_id) VALUES
-- ('Alice', 'Johnson', 'alice@company.com', '2020-03-15', 85000, 1),
-- ('Bob', 'Smith', 'bob@company.com', '2019-07-01', 72000, 1),
-- ('Carol', 'Williams', 'carol@company.com', '2021-01-10', 65000, 2),
-- ('David', 'Brown', 'david@company.com', '2018-11-20', 90000, 1),
-- ('Eve', 'Davis', 'eve@company.com', '2022-05-01', 55000, 3),
-- ('Frank', 'Miller', 'frank@company.com', '2020-09-15', 78000, 2),
-- ('Grace', 'Wilson', 'grace@company.com', '2021-06-01', 62000, 4),
-- ('Henry', 'Taylor', 'henry@company.com', '2019-03-01', 95000, 1);

-- INSERT INTO projects (project_name, start_date, end_date, budget, dept_id) VALUES
-- ('Website Redesign', '2024-01-01', '2024-06-30', 50000, 3),
-- ('Mobile App', '2024-02-15', '2024-12-31', 150000, 1),
-- ('Sales Portal', '2024-03-01', '2024-09-30', 75000, 2),
-- ('HR System', '2024-04-01', '2024-08-31', 40000, 4);


SELECT * FROM departments;
SELECT * FROM employees;
SELECT * FROM projects;

ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

ALTER TABLE departments ALTER COLUMN budget TYPE DECIMAL(15, 2); 


CREATE TABLE training_courses(
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    duration_hours INTEGER,
    instructor VARCHAR(100)
);


INSERT INTO employees
(first_name, last_name, email, salary)
VALUES
('Grace', 'Lee', 'grace.lee@company.com', 58000),
('Ivan', 'Chen', 'ivan@company.com', 61000),
('Julia', 'Kim', 'julia@company.com', 55000);


UPDATE employees
SET salary = salary * 1.10
WHERE dept_id = 1;


UPDATE employees
SET email='bob.smith@company.com'
WHERE first_name='Bob' AND last_name='Smith';


DELETE FROM projects
WHERE end_date < CURRENT_DATE;


SELECT * FROM employees
ORDER BY salary DESC;


SELECT * FROM employees
WHERE dept_id = 1;


SELECT * FROM employees
WHERE hire_date > '2022-12-31';


SELECT * FROM employees
WHERE salary > 60000 AND salary < 80000
ORDER BY salary DESC;



SELECT * FROM employees
WHERE email LIKE '%company%';


SELECT * FROM departments
WHERE location = 'Building A' OR location = 'Building B';



SELECT AVG(salary) FROM employees;
SELECT MIN(salary) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT dept_name, SUM(salary) 
FROM employees e JOIN departments d ON e.dept_id = d.dept_id
GROUP BY dept_name;


SELECT d.dept_name, Count(e.dept_id)
FROM employees e JOIN departments d 
    ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING Count(e.dept_id) > 2;

SELECT 
    e.first_name || ' ' || e.last_name AS full_name,
    d.dept_name AS department,
    ROUND(e.salary, 2) AS salary_formatted
FROM employees e JOIN departments d
    ON e.dept_id = d.dept_id;


SELECT * FROM employees
WHERE salary > (
    SELECT AVG(salary) FROM employees
);

SELECT dept_name
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM projects p
    WHERE p.dept_id = d.dept_id
);

SELECT * FROM departments;
SELECT * FROM employees;
SELECT * FROM projects;


SELECT MAX(salary)
FROM employees
GROUP BY dept_id;

-- Calculate how long each employee has been with the company (in years and months).
SELECT 
    first_name,
    last_name,
    hire_date,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, hire_date)) AS years_with_company,
    EXTRACT(MONTH FROM AGE(CURRENT_DATE, hire_date)) AS months_with_company
    FROM employees;
