# Northstar project — simple folder guide

## Project pipeline

SQL database → SQL queries → Python export → Python EDA → Power BI → AI dashboard

## Folder map

```text
northstar-project/
├── 01_SQL/
│   ├── schema.sql
│   ├── README.md
│   └── queries/
│       ├── 01_total_sales.sql
│       ├── 02_sales_by_region.sql
│       ├── 03_sales_by_product.sql
│       ├── 04_daily_sales_trend.sql
│       └── 05_more_practice_queries.sql
├── 02_Python_EDA/
│   ├── README.md
│   ├── 01_create_database.py
│   ├── seed.py
│   ├── 02_export_sql_to_csv.py
│   ├── 03_check_data.py
│   ├── 04_revenue_tables.py
│   └── 05_make_eda_charts.py
├── 03_PowerBI/
│   └── README.md
├── 04_AI_Dashboard/
│   ├── README.md
│   ├── app.py
│   └── static/
│       ├── index.html
│       └── app.js
├── data/
│   └── northstar.db
├── reports/
├── requirements.txt
└── start-northstar.bat
```

## Follow these steps

Open Command Prompt and go to the project folder:

    cd /d "C:\Users\DELL\Documents\Codex\2026-10-07\i-learned-eda-i-learned-ml\outputs\northstar-project"

Activate the virtual environment and install packages:

    python -m venv --upgrade .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt

The upgrade command refreshes the existing environment to use the Python installed on this computer.

Run each Python file from the main project folder, in this order:

    python 02_Python_EDA\01_create_database.py
    python 02_Python_EDA\02_export_sql_to_csv.py
    python 02_Python_EDA\03_check_data.py
    python 02_Python_EDA\04_revenue_tables.py
    python 02_Python_EDA\05_make_eda_charts.py

The Python files read from or write to the shared data and reports folders. Read the reports\eda_summary.txt file and open the chart images in reports.

## What do I do with the SQL files?

The SQL examples are in 01_SQL\queries. They are SQL code, so open/run them with a SQLite database viewer such as DB Browser for SQLite. Open data\northstar.db in that program. Start with 01_total_sales.sql. The table design is in 01_SQL\schema.sql. Do not type SQL filenames as Python commands.

## Power BI

Open Power BI Desktop. Choose Get data → Text/CSV, select reports\orders_for_powerbi.csv, then load it. Add a revenue card, date/revenue line chart, region/revenue pie chart, product/revenue bar chart, and date/region slicers. Save your report in 03_PowerBI as northstar-sales.pbix. See 03_PowerBI\README.md for those steps.

## AI dashboard

Run:

    python 04_AI_Dashboard\app.py

Open http://127.0.0.1:8000. On Overview, scroll down to Explore the data. The website files are in 04_AI_Dashboard\static. The dashboard reads the shared SQLite database. Its question bot uses sample-data analysis; without an API key it answers supported questions using built-in rules.

To stop the web server, press Ctrl+C in Command Prompt.

## Important

This project currently uses the included SQLite demo database. The Power BI CSV is an export snapshot. If data changes, rerun the Python export and EDA steps, then refresh the CSV in Power BI. The root .venv folder is your Python virtual environment; do not move it into one of the learning folders.

