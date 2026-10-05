from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_CSV_PATH = BASE_DIR / "data" / "raw" / "Telco-Customer-Churn.csv"
DB_PATH = BASE_DIR / "data" / "warehouse.db"
REPORTS_DIR = BASE_DIR / "reports"

SOURCE_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)

RAW_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
