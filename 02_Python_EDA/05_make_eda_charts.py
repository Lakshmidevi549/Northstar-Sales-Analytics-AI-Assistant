"""Step 5: create a trend line, region pie, order histogram, and product bar chart."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parent.parent
REPORTS = PROJECT / "reports"
CSV_FILE = REPORTS / "orders_for_powerbi.csv"
if not CSV_FILE.exists():
    raise SystemExit("CSV missing. First run: python 02_Python_EDA\\02_export_sql_to_csv.py")

data = pd.read_csv(CSV_FILE, parse_dates=["order_date"])

daily = data.groupby("order_date")["revenue"].sum()
daily.plot(figsize=(10, 5), color="#526cf2", title="Daily Revenue")
plt.xlabel("Order date"); plt.ylabel("Revenue ($)"); plt.tight_layout()
plt.savefig(REPORTS / "daily_revenue.png", dpi=150); plt.close()

regions = data.groupby("region")["revenue"].sum().sort_values(ascending=False)
regions.plot(kind="pie", figsize=(7, 6), autopct="%1.1f%%", title="Revenue Share by Region")
plt.ylabel(""); plt.tight_layout()
plt.savefig(REPORTS / "revenue_by_region_pie.png", dpi=150); plt.close()

data["revenue"].plot(kind="hist", bins=12, figsize=(9, 5), color="#8065df", title="Order Value Distribution")
plt.xlabel("Order revenue ($)"); plt.ylabel("Number of orders"); plt.tight_layout()
plt.savefig(REPORTS / "order_value_histogram.png", dpi=150); plt.close()

products = data.groupby("product")["revenue"].sum().nlargest(10).sort_values()
products.plot(kind="barh", figsize=(9, 6), color="#41ad8b", title="Top 10 Products by Revenue")
plt.xlabel("Revenue ($)"); plt.tight_layout()
plt.savefig(REPORTS / "top_products.png", dpi=150); plt.close()

print("Four charts created in the reports folder.")
