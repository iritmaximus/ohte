"""Defines global variable engine for making a connection to db"""
import sqlalchemy
import config

engine = sqlalchemy.create_engine(config.db_url(), echo=True)
