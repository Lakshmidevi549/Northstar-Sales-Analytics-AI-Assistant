-- SQL lesson 1: total orders, sales, average order value, and customers.
SELECT COUNT(*) AS order_count,
       ROUND(SUM(revenue), 2) AS total_revenue,
       ROUND(AVG(revenue), 2) AS average_order_value,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
