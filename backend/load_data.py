import sqlite3
import pandas as pd

conn = sqlite3.connect(
    "expense_tracker.db",
    check_same_thread=False
)

# ======================================================
# LOAD EXPENSE DATA
# ======================================================

def load_expense_data():

    query = """
    SELECT *
    FROM expenses
    """

    df = pd.read_sql(query, conn)

    df.rename(
        columns={
            "Withdrawal": "Withdrawal Amt."
        },
        inplace=True
    )

    return df