#!/usr/bin/python3
""" Module for City class """

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey

class City(BaseModel, Base):
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
