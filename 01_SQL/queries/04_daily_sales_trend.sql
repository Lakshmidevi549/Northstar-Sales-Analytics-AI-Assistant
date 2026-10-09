-- SQL lesson 4: see how revenue changes by date.
SELECT order_date, COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;
