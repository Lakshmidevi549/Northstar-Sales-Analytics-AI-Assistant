"""Step 4: group the data for simple region/product analysis."""
from pathlib import Path
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
REPORTS = PROJECT / "reports"
CSV_FILE = REPORTS / "orders_for_powerbi.csv"

if not CSV_FILE.exists():
    raise SystemExit("CSV missing. First run: python 02_Python_EDA\\02_export_sql_to_csv.py")

data = pd.read_csv(CSV_FILE)
by_region = data.groupby("region", as_index=False).agg(
    orders=("order_id", "nunique"), revenue=("revenue", "sum")
).sort_values("revenue", ascending=False)
by_product = data.groupby("product", as_index=False).agg(
    units=("quantity", "sum"), revenue=("revenue", "sum")
).sort_values("revenue", ascending=False)

by_region.to_csv(REPORTS / "revenue_by_region.csv", index=False)
by_product.to_csv(REPORTS / "revenue_by_product.csv", index=False)
print("Saved revenue_by_region.csv and revenue_by_product.csv in reports.")
