from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse  # This library fixes the password issue

# 1. We encode the password "1610" so the system doesn't get confused
encoded_password = urllib.parse.quote_plus("Sudheer@1610")

# 2. We put the encoded password into the connection string
# We also use '127.0.0.1' instead of 'localhost' to be safer on Windows
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@127.0.0.1/blog_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()