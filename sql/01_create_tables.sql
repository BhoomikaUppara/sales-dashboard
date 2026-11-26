CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
  row_id INT, order_id VARCHAR(20), order_date DATE, ship_date DATE,
  ship_mode VARCHAR(30), customer_id VARCHAR(20), customer_name VARCHAR(60),
  segment VARCHAR(20), country VARCHAR(30), state VARCHAR(40), region VARCHAR(20),
  category VARCHAR(30), sub_category VARCHAR(30), product_name VARCHAR(100),
  sales DECIMAL(12,2), quantity INT, discount DECIMAL(4,2), profit DECIMAL(12,2),
  order_year INT, order_month INT, month_name VARCHAR(5),
  profit_margin DECIMAL(8,4), shipping_days INT
);