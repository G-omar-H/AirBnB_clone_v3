#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
          }


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        returns a dictionary containing every object
        """
        if (not cls):
            return self.__objects
        result = {}
        for key in self.__objects.keys():
            if type(cls) is str:
                if (key.split(".")[0] == cls):
                    result.update({key: self.__objects[key]})
            else:
                if (key.split(".")[0] == cls.__name__):
                    result.update({key: self.__objects[key]})
        return result

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """
        delete obj from __objects if it's inside
            if obj is equal to None, the method do nothing
        """
        if obj is not None:
            k = [i for i in FileStorage.__objects
                 if FileStorage.__objects[i] == obj]
            for elem in k:
                del FileStorage.__objects[elem]

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """
        deserialize JSON file to object
        """
        self.reload()

    def get(self, cls, id):
        """
        returns object based on it's class and id
        None if not found
        Args:
            id (int): id of the class instance
            cls (obj): class object_
        """
        if cls in classes.values() and id and type(id) is str:
            d_obj = self.all(cls)
            for key, value in d_obj.items():
                if key.split(".")[1] == id:
                    return value
        return None

    def count(self, cls=None):
        """
        returns number of objects in storage matching the given class.
        if no class count number of all objects in storage

        Args:
            cls (_obj_, optional): class object to count. Defaults to None.
        """
        if cls:
            return len(self.all(cls))
        return len(self.all())
