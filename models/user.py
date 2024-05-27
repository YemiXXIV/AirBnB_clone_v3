#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        __password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")
    else:
        email = ""
        __password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """Returns the password of the user"""
        return self.__password

    @password.setter
    def password(self, value):
        """Hashing password values using md5 hash function"""
        self.__password = hashlib.md5(value.encode()).hexdigest()
