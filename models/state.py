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
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                lista.append(var[key])
        for elem in lista:
            if (elem.state_id == self.id):
                result.append(elem)
        return (result)
