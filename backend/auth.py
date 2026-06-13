from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:root123@localhost/expense_tracker"
)

with engine.connect() as conn:

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
    """))

    conn.commit()

# ======================================================
# CREATE USER
# ======================================================

def create_user(username, password):

    try:

        with engine.connect() as conn:

            conn.execute(
                text("""
                INSERT INTO users(username, password)
                VALUES(:username, :password)
                """),
                {
                    "username": username,
                    "password": password
                }
            )

            conn.commit()

        return True

    except:

        return False

# ======================================================
# LOGIN USER
# ======================================================

def login_user(username, password):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM users
            WHERE username=:username
            AND password=:password
            """),
            {
                "username": username,
                "password": password
            }
        )

        user = result.fetchone()

    return user