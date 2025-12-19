import os, json, requests
from loguru import logger
from config import Config
from db import fetch_data
from etl import transform_sales_data
from powerbi_client import get_client
from scheduler import schedule_job
import pandas as pd
from datetime import datetime

logger.remove()
logger.add('logs/app_{time:YYYY-MM-DD}.log', level=Config.LOG_LEVEL)

SQL_QUERY = """
SELECT sale_date, product_id, quantity, unit_price
FROM sales
WHERE sale_date >= date('now','-7 days')
"""

DATASET_NAME = "SalesPushDataset_Prototype"
TABLE_NAME = "SalesAggregated"

def run_once():
    try:
        logger.info("=== RUN START ===")
        df = fetch_data(SQL_QUERY)
        transformed = transform_sales_data(df)

        if transformed is None or len(transformed)==0:
            logger.warning("No data after transformation - nothing to push")
            return

        rows = []
        transformed = transformed.fillna('')
        for _, r in transformed.iterrows():
            row = {}
            for c in transformed.columns:
                val = r[c]
                if pd.isna(val):
                    val = None
                elif hasattr(val, 'to_pydatetime'):
                    val = str(val)
                else:
                    try:
                        val = val.item() if hasattr(val, 'item') else val
                    except Exception:
                        pass
                row[str(c)] = val
            rows.append(row)

        client = get_client()

        columns = {}
        for c in transformed.columns:
            if "date" in c.lower():
                columns[c] = "DateTime"
            elif transformed[c].dtype.kind in "i":
                columns[c] = "Int64"
            elif transformed[c].dtype.kind in "f":
                columns[c] = "Double"
            else:
                columns[c] = "string"

        ds = client.create_push_dataset(DATASET_NAME, TABLE_NAME, columns)
        dataset_id = ds.get('id', ds.get('name', DATASET_NAME))

        chunk_size = 5000
        for i in range(0, len(rows), chunk_size):
            batch = rows[i:i+chunk_size]
            client.add_rows(dataset_id, TABLE_NAME, batch)

        if Config.EXPORT_PDF and Config.WORKSPACE_ID and Config.REPORT_ID:
            result = client.export_report_to_file(Config.WORKSPACE_ID, Config.REPORT_ID, format='PDF')
            if result:
                fname = os.path.join('outputs', f"report_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.pdf")
                with open(fname, 'wb') as f:
                    f.write(result)
                logger.info(f'Exported report to {fname}')
        logger.info("=== RUN COMPLETE ===")
    except Exception as e:
        logger.exception("Run failed with exception")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--schedule', action='store_true')
    args = parser.parse_args()

    os.makedirs('outputs', exist_ok=True)

    if args.once:
        run_once()
    elif args.schedule:
        schedule_job(run_once, Config.SCHEDULE_CRON)
        logger.info('Scheduler started - press Ctrl+C to exit')
        try:
            import time
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info('Shutting down')
    else:
        run_once()
