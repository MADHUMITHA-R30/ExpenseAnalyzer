from sqlalchemy import create_engine, text

# ======================================================
# MYSQL CONNECTION
# ======================================================

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/expense_tracker"
)

# ======================================================
# CREATE EXPENSE TABLE
# ======================================================

with engine.connect() as conn:

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS expenses(
        Date TEXT,
        Month TEXT,
        Year INT,
        Category TEXT,
        Withdrawal FLOAT,
        Username TEXT
    )
    """))

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
        con=engine,
        if_exists="append",
        index=False
    )