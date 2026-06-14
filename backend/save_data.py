import sqlite3

conn = sqlite3.connect(
    "expense_tracker.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ======================================================
# CREATE EXPENSE TABLE
# ======================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    Date TEXT,
    Month TEXT,
    Year INTEGER,
    Category TEXT,
    Withdrawal REAL,
    Username TEXT
)
""")

conn.commit()

# ======================================================
# SAVE EXPENSE DATA
# ======================================================

def save_expense_data(df):

    df = df.copy()

    df.rename(
        columns={
            "Withdrawal Amt.": "Withdrawal"
        },
        inplace=True
    )

    df.to_sql(
        "expenses",
        conn,
        if_exists="append",
        index=False
    )