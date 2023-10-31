from . import db
from flask_login import *
from sqlalchemy import func, ForeignKeyConstraint
import enum

class User(db.Model, UserMixin):
    __table_name__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150))#, unique = True
    pwd = db.Column(db.String(150))
