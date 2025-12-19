import sqlite3, os, json, datetime
from config import Config
from ai_engine import generate_ai_summary
from powerbi_client import MockPowerBIClient
import plotly.graph_objects as go

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def run_pipeline():
    os.makedirs(Config.DATASETS_DIR, exist_ok=True)
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)

    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()
    c.execute("SELECT product, stock_level FROM stock")
    rows = c.fetchall()
    conn.close()

    stock_data = [{"Product": r[0], "Stock": r[1]} for r in rows]

    ts = timestamp()

    dataset_file = f"{Config.DATASETS_DIR}/dataset_{ts}.json"
    with open(dataset_file, "w") as f:
        json.dump(stock_data, f, indent=2)

    pbi = MockPowerBIClient()
    pbi.push(stock_data)

    fig = go.Figure(
        [go.Bar(x=[s["Product"] for s in stock_data],
                y=[s["Stock"] for s in stock_data])]
    )
    chart_path = f"{Config.REPORTS_DIR}/chart_{ts}.png"
    fig.write_image(chart_path)

    summary = generate_ai_summary(stock_data)

    html_path = f"{Config.REPORTS_DIR}/report_{ts}.html"
    with open(html_path, "w") as f:
        f.write(f"""
        <h1>Stock Report {ts}</h1>
        <pre>{summary}</pre>
        <img src="{os.path.basename(chart_path)}" width="700">
        """)

    print("Pipeline completed:", ts)
