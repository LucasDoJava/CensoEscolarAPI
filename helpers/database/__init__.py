import _sqlite3
from flask import g
import psycopg2

from helpers.application import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

db.init_app(app)

DATABASE = 'censoescolar'


def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            dbname=DATABASE,
            user='postgres',
            password='!@LuizInacio008',
            host='localhost',
            port='5432'
        )
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()