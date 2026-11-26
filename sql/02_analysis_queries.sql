USE sales_db;

-- 1. Core KPIs
SELECT ROUND(SUM(sales),2) AS total_sales,
       ROUND(SUM(profit),2) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders,
       COUNT(DISTINCT customer_id) AS total_customers,
       ROUND(SUM(profit)/SUM(sales)*100,2) AS profit_margin_pct
FROM sales;

-- 2. Region performance
SELECT region, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit
FROM sales GROUP BY region ORDER BY sales DESC;

-- 3. Top 10 products by sales
SELECT product_name, ROUND(SUM(sales),2) AS total_sales
FROM sales GROUP BY product_name ORDER BY total_sales DESC LIMIT 10;

-- 4. Monthly sales trend
SELECT order_year, order_month, ROUND(SUM(sales),2) AS monthly_sales
FROM sales GROUP BY order_year, order_month ORDER BY order_year, order_month;

-- 5. Category and sub-category profit
SELECT category, sub_category, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit
FROM sales GROUP BY category, sub_category ORDER BY profit DESC;

-- 6. Discount impact on margin
SELECT discount, ROUND(AVG(profit_margin)*100,2) AS avg_margin_pct, COUNT(*) AS line_items
FROM sales GROUP BY discount ORDER BY discount;

-- 7. Year over year growth
WITH yearly AS (SELECT order_year, SUM(sales) AS s FROM sales GROUP BY order_year)
SELECT order_year, ROUND(s,2) AS sales,
       ROUND((s - LAG(s) OVER (ORDER BY order_year)) /
              LAG(s) OVER (ORDER BY order_year) * 100, 2) AS yoy_growth_pct
FROM yearly;

-- 8. Top 10 customers
SELECT customer_name, COUNT(DISTINCT order_id) AS orders, ROUND(SUM(sales),2) AS total_spent
FROM sales GROUP BY customer_name ORDER BY total_spent DESC LIMIT 10;

-- 9. Segment performance
SELECT segment, ROUND(SUM(sales),2) AS sales, ROUND(SUM(profit),2) AS profit
FROM sales GROUP BY segment ORDER BY sales DESC;