from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection String Format: 
# mssql+pyodbc://<username>:<password>@<dsnname>?driver=ODBC+Driver+17+for+SQL+Server
# If using Windows Authentication (Trusted Connection), use this:
SERVER_NAME = 'DESKTOP-IM92AEE\\SQLEXPRESS' 
DATABASE_NAME = 'MUDemy'
CONNECTION_STRING = f'mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
USERNAME = "student123"
PASSWORD = "Pass123!"

# CONNECTION_STRING = (
#     f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER_NAME}/{DATABASE_NAME}"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
# )
# Create the Engine
engine = create_engine(CONNECTION_STRING, echo=False) # Set echo=True to see generated SQL in console

# Test connection
try:
    with engine.connect() as conn:
        # result = conn.execute(
        #     text("EXEC CreateMngUserForApp @LoginName=:login, @Password=:pwd"),
        #     {"login": "sManager", "pwd": "toi_yeu_phaothu"}
        # )
        result = conn.execute(text("SELECT * FROM [USER]"))
        print("✅ Database connection successful!")

        print("Result:",result.fetchall())
except Exception as e:
    print("❌ Database connection failed!")
    print("Error:", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session (useful for API dependency injection later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


