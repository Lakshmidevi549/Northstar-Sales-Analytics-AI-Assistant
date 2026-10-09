"""Step 2: read rows from SQLite using SQL and export a CSV for Python/Power BI."""
from pathlib import Path
import csv
import sqlite3

PROJECT = Path(__file__).resolve().parent.parent
DATABASE = PROJECT / "data" / "northstar.db"
OUTPUT = PROJECT / "reports" / "orders_for_powerbi.csv"

QUERY = """
SELECT order_id, order_date, customer_id, region, product, category,
       quantity, revenue, returning_customer
FROM orders
ORDER BY order_date;
"""

if not DATABASE.exists():
    raise SystemExit("Database missing. First run: python 02_Python_EDA\\01_create_database.py")

OUTPUT.parent.mkdir(exist_ok=True)
with sqlite3.connect(DATABASE) as connection:
    cursor = connection.execute(QUERY)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

with OUTPUT.open("w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"Exported {len(rows):,} rows to: {OUTPUT}")
