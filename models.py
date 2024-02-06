import databases
import datetime
from sqlalchemy import Table, Column, String, Integer, create_engine, MetaData, ForeignKey, Boolean, Float
from pydantic import BaseModel

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

items = Table(
    'items',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64)),
    Column('description', String(512)),
    Column('price', Integer),
    Column('discount', Float, default=0.9),
    Column('is_active', Boolean, default=True)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String(16)),
    Column('last_name', String(16)),
    Column('email', String(64)),
    Column('hashed_password', String),
    Column('is_active', Boolean, default=True)
)

orders = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_user', Integer, ForeignKey('users.id')),
    Column('id_item', Integer, ForeignKey('items.id')),
    Column('date', String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
    Column('is_active', Boolean, default=True)
)

engine = create_engine(DATABASE_URL)
