#!/usr/bin/python3
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class City(BaseModel, Base):
    """Representation of city """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete-orphan")
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        if 'created_at' in kwargs and isinstance(kwargs['created_at'], str):
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        if 'updated_at' in kwargs and isinstance(kwargs['updated_at'], str):
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
        super().__init__(*args, **kwargs)

