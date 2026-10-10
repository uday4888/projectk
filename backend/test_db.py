from database import engine

try:
    with engine.connect() as connection:
        print("MySQL connection successful!")
except Exception as error:
    print("MySQL connection failed:", error)