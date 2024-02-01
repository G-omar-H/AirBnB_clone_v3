#!/usr/bin/python3
"""
        storage data engine
        MySQL DataBase
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


class DBStorage:
    """
    MySQl DataBase engine class ORM
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        initialization...
        """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        all objects depending of the class name (argument cls)
        """
        obj_dict = {}
        objs_list = ["User", "State", "City", "Place", "Amenity", "Review"]
        objs = []
        if cls is not None:
            objs.extend(self.__session.query(cls).all())
        else:
            for table_name in objs_list:
                objs.extend(self.__session.query(table_name).all())
        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        add the object to the current database session.
        """
        self.__session.add(obj)
        self.__session.flush()

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database and the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        close a connected  session
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        self.__session.close()
