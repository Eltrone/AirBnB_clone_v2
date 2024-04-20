#!/usr/bin/python3
""" Module for State class """

from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type  # Supposons que vous avez défini cela quelque part dans le module de configuration

class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if storage_type == 'db':
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        @property
        def cities(self):
            """Return the list of City objects from storage linked to the current State."""
            from models import storage
            from models.city import City
            all_cities = storage.all(City)
            return [city for city in all_cities.values() if city.state_id == self.id]
