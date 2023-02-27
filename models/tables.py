#!/usr/bin/python3
"""Database models"""
from sqlalchemy import engine, Table
from sqlalchemy import MetaData, select
from sqlalchemy.orm import Session
import os
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASS')
db = os.getenv('MYSQL_DB')
meta = MetaData()
my_engine = engine.create_engine(
        'mysql+pymysql://{}:{}@localhost/{}'
        .format(user, password, db))
driver = Session(bind=my_engine)
states = Table('states', meta, autoload_with=my_engine)
lgas = Table('lga', meta, autoload_with=my_engine)
ward = Table('ward', meta, autoload_with=my_engine)
polling_unit = Table('polling_unit', meta, autoload_with=my_engine)
announced_pu_results =Table('announced_pu_results', meta,
            autoload_with=my_engine)
party = Table('party', meta, autoload_with=my_engine)
meta.create_all(my_engine)
