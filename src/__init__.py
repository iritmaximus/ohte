"""Defines global variable engine for making a connection to db"""
import sqlalchemy
from src import config

engine = sqlalchemy.create_engine(config.db_url(), echo=True)
