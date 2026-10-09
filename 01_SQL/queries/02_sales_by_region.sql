-- SQL lesson 2: compare revenue and order counts by region.
SELECT region, COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY region
ORDER BY revenue DESC;
