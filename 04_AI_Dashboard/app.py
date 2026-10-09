from __future__ import annotations
import json, os, re, sqlite3, urllib.request
from datetime import date, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv('DATABASE_PATH', ROOT / 'data' / 'northstar.db'))
STATIC = ROOT / '04_AI_Dashboard' / 'static'

# Read a local .env file for convenience; environment variables take precedence.
for line in (ROOT / '.env').read_text(encoding='utf-8').splitlines() if (ROOT / '.env').exists() else []:
    if line.strip() and not line.lstrip().startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"\''))


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def overview(days=30, region='all'):
    days = min(max(int(days), 1), 365)
    start = (date.today() - timedelta(days=days - 1)).isoformat()
    con = db()
    where = 'order_date >= ?'
    params = [start]
    if region != 'all':
        where += ' AND region = ?'
        params.append(region)
    total = con.execute(f'''SELECT COUNT(*) orders, COALESCE(SUM(revenue),0) revenue,
        COUNT(DISTINCT customer_id) customers,
        SUM(CASE WHEN returning_customer=1 THEN 1 ELSE 0 END) returning_orders
        FROM orders WHERE {where}''', params).fetchone()
    daily = con.execute(f'''SELECT order_date, ROUND(SUM(revenue),2) revenue, COUNT(*) orders
        FROM orders WHERE {where} GROUP BY order_date ORDER BY order_date''', params).fetchall()
    by_region = con.execute(f'''SELECT region, ROUND(SUM(revenue),2) revenue, COUNT(*) orders
        FROM orders WHERE order_date >= ? GROUP BY region ORDER BY revenue DESC''', [start]).fetchall()
    products = con.execute(f'''SELECT product, category, SUM(quantity) units, ROUND(SUM(revenue),2) revenue
        FROM orders WHERE {where} GROUP BY product, category ORDER BY revenue DESC LIMIT 8''', params).fetchall()
    histogram = con.execute(f'''SELECT band,
        CASE band WHEN 1 THEN '< $50' WHEN 2 THEN '$50-$99' WHEN 3 THEN '$100-$149'
                  WHEN 4 THEN '$150-$199' ELSE '$200+' END bucket,
        COUNT(*) orders
        FROM (SELECT CASE WHEN revenue < 50 THEN 1 WHEN revenue < 100 THEN 2
                          WHEN revenue < 150 THEN 3 WHEN revenue < 200 THEN 4 ELSE 5 END band
              FROM orders WHERE {where})
        GROUP BY band ORDER BY band''', params).fetchall()
    all_revenue = sum(r['revenue'] for r in by_region) or 1
    top_region = by_region[0] if by_region else {'region':'No data','revenue':0}
    top_product = products[0] if products else {'product':'No data','revenue':0}
    result = {
      'period_days': days, 'region': region,
      'metrics': {'revenue': round(total['revenue'],2), 'orders': total['orders'],
                  'aov': round(total['revenue']/total['orders'],2) if total['orders'] else 0,
                  'returning_rate': round(100*total['returning_orders']/total['orders'],1) if total['orders'] else 0,
                  'customers': total['customers']},
      'daily': [dict(r) for r in daily],
      'regions': [dict(r, share=round(100*r['revenue']/all_revenue,1)) for r in by_region],
      'products': [dict(r) for r in products],
      'histogram': [dict(r) for r in histogram],
      'insights': {'top_region': top_region['region'], 'top_product': top_product['product'],
                   'top_product_revenue': top_product['revenue'],
                   'regional_mix': [dict(r, share=round(100*r['revenue']/all_revenue,1)) for r in by_region]}
    }
    con.close()
    return result


def ask(question, context):
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-5.6-luna'),
                instructions=('You are Northstar, a careful business data analyst. Answer only from the JSON analysis provided. '
                               'Do not invent values or claim causation. If the data does not answer the question, say what is missing. '
                               'Use a concise explanation and include the relevant metric as evidence.'),
                input='Analysis JSON:\n' + json.dumps(context) + '\n\nUser question: ' + question)
            return {'answer': response.output_text, 'source': 'SQL analysis + OpenAI', 'mode':'ai'}
        except Exception as exc:
            return {'answer': f'AI request could not be completed ({type(exc).__name__}). Configure OPENAI_API_KEY and check network access.', 'source':'Configuration', 'mode':'error'}
    q = question.lower()
    m, i = context['metrics'], context['insights']
    if any(w in q for w in ('region','country','geograph')):
        rows = context['regions']
        ans = (f"{rows[0]['region']} leads with ${rows[0]['revenue']:,.2f} ({rows[0]['share']}% of regional revenue). "
               f"{i['top_region']} is the top region in the selected period.") if rows else 'There is no regional data for those filters.'
        source = 'SQL: revenue grouped by region'
    elif any(w in q for w in ('product','item','sell','top')):
        rows = context['products']
        ans = (f"{rows[0]['product']} is the top product with ${rows[0]['revenue']:,.2f} revenue and {rows[0]['units']} units.") if rows else 'There are no product rows for those filters.'
        source = 'SQL: revenue and units grouped by product'
    elif any(w in q for w in ('return','retention','customer','repeat')):
        ans = f"There were {m['customers']:,} distinct customers. Returning orders were {m['returning_rate']}% of orders in this period."
        source = 'SQL: distinct customers and returning order rate'
    elif any(w in q for w in ('order','average','aov')):
        ans = f"There were {m['orders']:,} orders with an average order value of ${m['aov']:,.2f}."
        source = 'SQL: order count and revenue per order'
    else:
        ans = (f"Revenue was ${m['revenue']:,.2f} across {m['orders']:,} orders. Average order value was ${m['aov']:,.2f}; "
               f"returning order rate was {m['returning_rate']}%. Ask about regions, products, customers, or orders for a breakdown.")
        source = 'SQL: overview metrics'
    return {'answer':ans, 'source':source, 'mode':'rules'}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(STATIC), **kwargs)
    def log_message(self, fmt, *args): print('%s - %s' % (self.log_date_time_string(), fmt % args))
    def send_json(self, status, body):
        raw=json.dumps(body).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path=='/api/health':
            return self.send_json(200, {'ok':True,'database':'sqlite','ai_enabled':bool(os.getenv('OPENAI_API_KEY'))})
        if parsed.path=='/api/overview':
            q=parse_qs(parsed.query)
            try: return self.send_json(200, overview(q.get('days',['30'])[0], q.get('region',['all'])[0]))
            except Exception as exc: return self.send_json(500, {'error':str(exc)})
        if parsed.path=='/': self.path='/index.html'
        return super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!='/api/ask': return self.send_json(404, {'error':'Not found'})
        try:
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            question=str(data.get('question','')).strip()
            if not question or len(question)>500: return self.send_json(400, {'error':'Question must be 1–500 characters.'})
            context=overview(data.get('days',30), data.get('region','all'))
            return self.send_json(200, ask(question,context))
        except Exception as exc: return self.send_json(500, {'error':str(exc)})
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS'); self.end_headers()

if __name__=='__main__':
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    if not DB_PATH.exists():
        raise SystemExit(f'Database not found at {DB_PATH}. Run: python 02_Python_EDA\\01_create_database.py')
    host=os.getenv('HOST','127.0.0.1'); port=int(os.getenv('PORT','8000'))
    print(f'Northstar running at http://{host}:{port}  (Ctrl+C to stop)')
    ThreadingHTTPServer((host,port),Handler).serve_forever()

