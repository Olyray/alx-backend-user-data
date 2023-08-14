#!/usr/bin/env python3
"""Implementation of user"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """A class user"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(length=250), nullable=False)
    hashed_password = Column(String(length=250), nullable=False)
    session_id = Column(String(length=250), nullable=True)
    reset_token = Column(String(length=250), nullable=True)
