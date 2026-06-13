from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/expense_tracker"
)