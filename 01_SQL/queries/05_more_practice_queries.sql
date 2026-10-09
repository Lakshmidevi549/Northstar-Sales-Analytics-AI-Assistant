-- Northstar sales EDA queries (SQLite)
-- Open data/northstar.db in a SQLite tool, or use these queries as learning examples.

-- 1) Overall KPI check
SELECT COUNT(*) AS order_count,
       ROUND(SUM(revenue), 2) AS total_revenue,
       ROUND(AVG(revenue), 2) AS average_order_value,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;

-- 2) Daily sales trend
SELECT order_date, COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- 3) Regional revenue and percentage of total
SELECT region,
       COUNT(*) AS orders,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM orders), 1) AS revenue_share_pct
FROM orders
GROUP BY region
ORDER BY revenue DESC;

-- 4) Product and category performance
SELECT category, product,
       SUM(quantity) AS units_sold,
       ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY category, product
ORDER BY revenue DESC;

-- 5) Order-value histogram buckets
SELECT CASE
         WHEN revenue < 50 THEN '< $50'
         WHEN revenue < 100 THEN '$50-$99'
         WHEN revenue < 150 THEN '$100-$149'
         WHEN revenue < 200 THEN '$150-$199'
         ELSE '$200+'
       END AS order_value_band,
       COUNT(*) AS order_count
FROM orders
GROUP BY CASE
           WHEN revenue < 50 THEN 1
           WHEN revenue < 100 THEN 2
           WHEN revenue < 150 THEN 3
           WHEN revenue < 200 THEN 4
           ELSE 5
         END
ORDER BY 1;

-- 6) Repeat-order flag comparison
SELECT returning_customer,
       COUNT(*) AS order_count,
       ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY returning_customer;
