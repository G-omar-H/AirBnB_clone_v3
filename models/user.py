#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
import hashlib
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = "users"
    if storage_type == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship("Place", backref="user", cascade="all,delete")
        reviews = relationship("Review", backref="user", cascade="all,delete")
        password = hashlib.md5(password)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        password = hashlib.md5(password)
