from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/expense_tracker"
)

# ======================================================
# LOAD EXPENSE DATA
# ======================================================

def load_expense_data():

    query = """
    SELECT *
    FROM expenses
    """

    df = pd.read_sql(query, engine)

    df.rename(
        columns={
            "Withdrawal": "Withdrawal Amt."
        },
        inplace=True
    )

    return df