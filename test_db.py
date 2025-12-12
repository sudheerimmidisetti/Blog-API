# test_db.py
import sys
import urllib.parse
from sqlalchemy import create_engine, text

# EDIT THIS LINE WITH YOUR PASSWORD
password_str = "Sudheer@1610" 

print("--- Testing Database Connection ---")
encoded_pass = urllib.parse.quote_plus(password_str)
url = f"mysql+pymysql://root:{encoded_pass}@127.0.0.1/blog_db"

print(f"Attempting to connect to: mysql+pymysql://root:****@127.0.0.1/blog_db")

try:
    engine = create_engine(url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Success!'"))
        print("✅ Connection Successful!")
        print("Result:", result.scalar())
except Exception as e:
    print("\n❌ Connection Failed.")
    print("Error Details:", e)