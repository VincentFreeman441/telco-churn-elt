"""TRANSFORM: clean the raw table with SQL, inside the database (the 'T' in ELT)."""
import sqlite3

from config import DB_PATH

CLEAN_SQL = """
DROP TABLE IF EXISTS clean_customers;
CREATE TABLE clean_customers AS
SELECT
    customerID,
    tenure,
    Contract,
    MonthlyCharges,
    CASE WHEN TRIM(TotalCharges) = '' THEN 0
         ELSE CAST(TotalCharges AS REAL) END AS TotalCharges,
    CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS churned
FROM raw_customers;
"""

CHURN_BY_CONTRACT_SQL = """
DROP TABLE IF EXISTS churn_by_contract;
CREATE TABLE churn_by_contract AS
SELECT
    Contract,
    COUNT(*) AS customers,
    ROUND(AVG(churned), 4) AS churn_rate,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM clean_customers
GROUP BY Contract;
"""


def run() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(CLEAN_SQL)
        conn.executescript(CHURN_BY_CONTRACT_SQL)
    print("[TRANSFORM] built clean_customers, churn_by_contract")


if __name__ == "__main__":
    run()
