"""Defines global variable engine for making a connection to db"""
import sys
import sqlalchemy
from dotenv import load_dotenv
from src import config

load_dotenv()


engine = sqlalchemy.create_engine(config.db_url(), echo=config.env() == "production")

with engine.connect() as conn:
    conn.execute(sqlalchemy.text(open("./src/sql/schema.sql", "r").read()))
    conn.commit()
