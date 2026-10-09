PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  order_date TEXT NOT NULL,
  customer_id INTEGER NOT NULL,
  region TEXT NOT NULL,
  product TEXT NOT NULL,
  category TEXT NOT NULL,
  quantity INTEGER NOT NULL CHECK(quantity > 0),
  revenue REAL NOT NULL CHECK(revenue >= 0),
  returning_customer INTEGER NOT NULL DEFAULT 0 CHECK(returning_customer IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region);
CREATE INDEX IF NOT EXISTS idx_orders_product ON orders(product);
