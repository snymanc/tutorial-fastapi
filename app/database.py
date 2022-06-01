import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://" + \
                          f"{settings.database_username}:" + \
                          f"{settings.database_password}@" + \
                          f"{settings.database_hostname}:" + \
                          f"{settings.database_port}/" + \
                          f"{settings.database_name}"

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
            host=f"{settings.database_hostname}",
            database=f"{settings.database_name}",
            user=f"{settings.database_username}",
            password=f"{settings.database_password}",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("DB connection was successful")
        break
    except Exception as error:
        print("DB Connection failure:")
        print("Error: ", error)
        time.sleep(2)
