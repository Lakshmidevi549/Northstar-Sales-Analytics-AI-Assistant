import random, sqlite3
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/'data'/'northstar.db'
DB.parent.mkdir(parents=True, exist_ok=True)
random.seed(27)
products=[('Wireless Headphones','Electronics',74),('Everyday Backpack','Accessories',70),('Smart Watch Series 4','Electronics',86),('Ceramic Pour-over Set','Home & Living',55),('Travel Organizer Kit','Accessories',37),('Desk Lamp Pro','Home & Living',62),('Bluetooth Speaker Mini','Electronics',49),('Canvas Tote','Accessories',29)]
regions=['North America','Europe','Asia Pacific','Latin America']
weights=[42,27,19,12]
con=sqlite3.connect(DB)
con.executescript((ROOT/'01_SQL'/'schema.sql').read_text(encoding='utf-8'))
con.execute('DELETE FROM orders')
start=date.today()-timedelta(days=89)
rows=[]
for n in range(1800):
    day=start+timedelta(days=random.randrange(90))
    product,category,price=random.choice(products)
    quantity=random.choices([1,2,3],[.72,.23,.05])[0]
    region=random.choices(regions,weights=weights)[0]
    customer=random.randrange(1,881)
    returning=1 if customer<=410 and random.random()<.70 else 0
    revenue=round(price*quantity*random.uniform(.88,1.12),2)
    rows.append((f'ORD-{n+1:05}',day.isoformat(),customer,region,product,category,quantity,revenue,returning))
con.executemany('INSERT INTO orders(order_id,order_date,customer_id,region,product,category,quantity,revenue,returning_customer) VALUES(?,?,?,?,?,?,?,?,?)',rows)
con.commit();con.close()
print(f'Created {DB} with {len(rows)} demo orders.')
