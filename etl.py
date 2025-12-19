import pandas as pd
from loguru import logger

def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting transformation")
    df = df.copy()
    if 'sale_date' in df.columns:
        df['sale_date'] = pd.to_datetime(df['sale_date'])
    for col in ['quantity', 'unit_price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if 'quantity' in df.columns and 'unit_price' in df.columns:
        df['total_price'] = df['quantity'] * df['unit_price']
    if set(['sale_date', 'product_id', 'total_price']).issubset(df.columns):
        agg = df.groupby([df['sale_date'].dt.date, 'product_id'], as_index=False).agg({
            'quantity': 'sum',
            'total_price': 'sum'
        }).rename(columns={'sale_date': 'date'})
        logger.info(f"Transformed into {len(agg)} aggregated rows")
        return agg
    logger.info("No aggregation performed - returning cleaned frame")
    return df
