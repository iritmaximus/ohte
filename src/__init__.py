"""Defines global variable engine for making a connection to db"""
import sqlalchemy
import sys
from dotenv import load_dotenv

load_dotenv()

from src import config


engine = sqlalchemy.create_engine(config.db_url(), echo=config.env() != "production")
