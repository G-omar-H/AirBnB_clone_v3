#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
import hashlib
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")
m = hashlib.md5()


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
    else:
        email = ""
        password = b""
        first_name = ""
        last_name = ""

    def __setattr__(self, k, v):
        """sets user pasword"""
        if k == "password":
            v = hashlib.md5(v.encode()).hexdigest()
        super().__setattr__(k, v)
