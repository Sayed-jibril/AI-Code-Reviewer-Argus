-- SQL test file with various issues

-- Potentially destructive DDL
DROP TABLE users;

-- Overly broad GRANT
GRANT ALL ON database.* TO 'user'@'%';

-- SELECT * harms performance/clarity
SELECT * FROM users WHERE active = 1;

-- DELETE/UPDATE without WHERE (dangerous)
DELETE FROM logs;
UPDATE users SET last_login = NOW();

-- Check indexing on filtered columns
SELECT * FROM orders WHERE customer_id = 123;

-- More issues
SELECT * FROM products WHERE category = 'electronics';
UPDATE products SET price = price * 1.1;
