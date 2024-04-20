#!/usr/bin/python3
"""file serialization-deserialization"""

import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects if cls=None, else returns instances of cls."""
        if cls is None:
            return self.__objects
        else:
            cls_objects = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    cls_objects[key] = value
            return cls_objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def _serialize_obj(self, obj):
        """Converts recursively objects into a JSON serializable format."""
        if isinstance(obj, dict):
            return {k: self._serialize_obj(v) for k, v in obj.items()}
        elif hasattr(obj, "__dict__"):
            obj_dict = obj.__dict__.copy()
            obj_dict.pop('_sa_instance_state', None)
            for key, value in obj_dict.items():
                obj_dict[key] = self._serialize_obj(value)
            return obj_dict
        elif isinstance(obj, list):
            return [self._serialize_obj(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {obj_id: self._serialize_obj(obj) for obj_id, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists."""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                obj_dict = json.load(f)
                for obj_id, obj_attrs in obj_dict.items():
                    cls_name = obj_attrs["__class__"]
                    cls = eval(cls_name)
                    self.__objects[obj_id] = cls(**obj_attrs)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            print("Warning: file.json is empty or corrupt, starting with empty storage.")

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside."""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in self.__objects:
            del self.__objects[key]

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()
