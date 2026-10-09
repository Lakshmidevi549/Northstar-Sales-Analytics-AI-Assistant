-- SQL lesson 3: compare units and revenue by product.
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC;
