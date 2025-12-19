import os

class Config:
    DB_PATH = "demo.db"

    OUTPUTS_DIR = "outputs"
    DATASETS_DIR = "outputs/datasets"
    REPORTS_DIR = "outputs/reports"
    LOGS_DIR = "logs"

    UPDATE_INTERVAL_MINUTES = 5

    POWER_BI_URL = os.getenv("POWER_BI_URL", "")
    POWER_BI_TOKEN = os.getenv("POWER_BI_TOKEN", "")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
