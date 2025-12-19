from sqlalchemy import create_engine, text
import pandas as pd
from loguru import logger
from config import Config

def get_engine():
    engine = create_engine(Config.SQL_CONNECTION, echo=False)
    return engine

def fetch_data(query: str, params: dict = None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        logger.info('Executing query to fetch data')
        df = pd.read_sql_query(text(query), conn, params=params)
    logger.info(f'Fetched {len(df)} rows')
    return df
