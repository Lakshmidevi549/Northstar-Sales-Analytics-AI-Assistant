"""Run a beginner-friendly EDA workflow on the project's SQLite sales table.
Creates CSV exports, a text summary, and PNG charts under reports/.
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / 'data' / 'northstar.db'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

SQL = '''
SELECT order_id, order_date, customer_id, region, product, category,
       quantity, revenue, returning_customer
FROM orders
ORDER BY order_date;
'''


def main():
    if not DB_PATH.exists():
        raise SystemExit('Database not found. First run: python seed.py')

    # 1. Load from SQL into a pandas DataFrame.
    with sqlite3.connect(DB_PATH) as connection:
        df = pd.read_sql_query(SQL, connection)
    if df.empty:
        raise SystemExit('The orders table is empty. Run: python seed.py')
    df['order_date'] = pd.to_datetime(df['order_date'])

    # 2. Basic EDA checks.
    missing = df.isna().sum()
    duplicates = int(df['order_id'].duplicated().sum())
    summary = [
        'NORTHSTAR SALES EDA SUMMARY',
        '=' * 30,
        f'Rows: {len(df):,}',
        f'Columns: {len(df.columns)}',
        f'Date range: {df.order_date.min().date()} to {df.order_date.max().date()}',
        f'Duplicate order IDs: {duplicates}',
        f'Missing values total: {int(missing.sum())}',
        f'Total revenue: ${df.revenue.sum():,.2f}',
        f'Total orders: {df.order_id.nunique():,}',
        f'Average order value: ${df.revenue.mean():,.2f}',
        f'Distinct customers: {df.customer_id.nunique():,}',
        '',
        'MISSING VALUES BY COLUMN',
        missing.to_string(),
        '',
        'NUMERIC DESCRIPTION',
        df[['quantity', 'revenue']].describe().round(2).to_string(),
        '',
        'REVENUE BY REGION',
        df.groupby('region').revenue.sum().sort_values(ascending=False).round(2).to_string(),
        '',
        'REVENUE BY CATEGORY',
        df.groupby('category').revenue.sum().sort_values(ascending=False).round(2).to_string(),
        '',
        'TOP 10 PRODUCTS BY REVENUE',
        df.groupby('product').revenue.sum().sort_values(ascending=False).head(10).round(2).to_string(),
    ]
    (REPORTS / 'eda_summary.txt').write_text('\n'.join(summary), encoding='utf-8')

    # 3. Export clean detail for Power BI and grouped summaries for inspection.
    df.to_csv(REPORTS / 'orders_for_powerbi.csv', index=False, date_format='%Y-%m-%d')
    df.groupby('region', as_index=False).agg(orders=('order_id', 'nunique'), revenue=('revenue', 'sum')).to_csv(REPORTS / 'revenue_by_region.csv', index=False)
    df.groupby('product', as_index=False).agg(units=('quantity', 'sum'), revenue=('revenue', 'sum')).sort_values('revenue', ascending=False).to_csv(REPORTS / 'revenue_by_product.csv', index=False)

    # 4. Create common EDA visuals.
    daily = df.groupby('order_date', as_index=False).revenue.sum()
    plt.figure(figsize=(10, 5)); plt.plot(daily.order_date, daily.revenue, color='#526cf2', linewidth=2)
    plt.title('Daily Revenue'); plt.xlabel('Order date'); plt.ylabel('Revenue ($)'); plt.grid(alpha=.2); plt.tight_layout()
    plt.savefig(REPORTS / 'daily_revenue.png', dpi=150); plt.close()

    by_region = df.groupby('region').revenue.sum().sort_values(ascending=False)
    plt.figure(figsize=(7, 6)); plt.pie(by_region, labels=by_region.index, autopct='%1.1f%%', startangle=90)
    plt.title('Revenue Share by Region'); plt.tight_layout(); plt.savefig(REPORTS / 'revenue_by_region_pie.png', dpi=150); plt.close()

    plt.figure(figsize=(9, 5)); plt.hist(df.revenue, bins=12, color='#8065df', edgecolor='white')
    plt.title('Order Value Distribution'); plt.xlabel('Order revenue ($)'); plt.ylabel('Number of orders'); plt.grid(axis='y', alpha=.2); plt.tight_layout()
    plt.savefig(REPORTS / 'order_value_histogram.png', dpi=150); plt.close()

    top = df.groupby('product').revenue.sum().sort_values(ascending=True).tail(10)
    plt.figure(figsize=(9, 6)); top.plot(kind='barh', color='#41ad8b')
    plt.title('Top 10 Products by Revenue'); plt.xlabel('Revenue ($)'); plt.tight_layout()
    plt.savefig(REPORTS / 'top_products.png', dpi=150); plt.close()

    print('EDA finished. Open the reports folder for the summary, Power BI CSV, and four charts.')
    print(f'Rows analyzed: {len(df):,} | Revenue: ${df.revenue.sum():,.2f} | AOV: ${df.revenue.mean():,.2f}')
    print(f'Report folder: {REPORTS}')

if __name__ == '__main__':
    main()
