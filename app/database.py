import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:GarthNeele@localhost/fastapi2"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi2",
            user="postgres",
            password="GarthNeele",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        print("DB Connection failure:")
        print("Error: ", error)
        time.sleep(2)
