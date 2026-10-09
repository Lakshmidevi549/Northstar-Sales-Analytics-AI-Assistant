"""Step 3: beginner EDA checks: shape, missing values, duplicates, and statistics."""
from pathlib import Path
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT / "reports" / "orders_for_powerbi.csv"
REPORT_FILE = PROJECT / "reports" / "eda_summary.txt"

if not CSV_FILE.exists():
    raise SystemExit("CSV missing. First run: python 02_Python_EDA\\02_export_sql_to_csv.py")

data = pd.read_csv(CSV_FILE, parse_dates=["order_date"])
missing = data.isna().sum()
duplicate_ids = int(data["order_id"].duplicated().sum())

summary = [
    "NORTHSTAR DATA CHECK",
    "====================",
    f"Rows: {len(data):,}",
    f"Columns: {len(data.columns)}",
    f"Date range: {data.order_date.min().date()} to {data.order_date.max().date()}",
    f"Missing cells: {int(missing.sum())}",
    f"Duplicate order IDs: {duplicate_ids}",
    f"Total revenue: ${data.revenue.sum():,.2f}",
    f"Average order value: ${data.revenue.mean():,.2f}",
    "",
    "Missing values by column:",
    missing.to_string(),
    "",
    "Numeric column statistics:",
    data[["quantity", "revenue"]].describe().round(2).to_string(),
]
REPORT_FILE.write_text("\n".join(summary), encoding="utf-8")
print("Data checks complete. Read reports\\eda_summary.txt")
