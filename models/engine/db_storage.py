#!/usr/bin/Python3
"""Contains the class for MySQL database storage"""
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)

user = os.getenv('HBNB_MYSQL_USER')
pwd = os.getenv('HBNB_MYSQL_PWD')
host = os.getenv('HBNB_MYSQL_HOST')
db = os.getenv('HBNB_MYSQL_DB')
env = os.getenv('HBNB_ENV')


class DBStorage:
    """Connects with the MySQL Database"""

    __classes = [State, City, User, Place, Review, Amenity]
    __engine = None
    __session = None

    def __init__(self):
        """Instance for the DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
    if env == "test":
        Base.MetaData.drop_all()

    def all(self, cls=None):
        """Method for current database session"""
        mydict_new = {}
        if cls in self.__classes:
            answer = DBStorage.__session.query(cls)
            for row in answer:
                key = "{}.{}".format(row.__class__.__name__, row.id)
                mydict_new[key] = row
        elif cls is None:
            for cl in self.__classes:
                answer = DBStorage.__session.query(cl)
                for row in answer:
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    mydict_new[key] = row
        return (mydict_new)

    def new(self, obj):
        """Add a new object to the current database"""
        DBStorage.__session.add(obj)

    def save(self):
        """Save all changes to the current database"""
        DBStorage.__session.commit()

    def delete(self, obj=None):
        """Delete a new object to the current database"""
        DBStorage.__session.delete(obj)

    def reload(self):
        """Reload data from the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        DBStorage.__session = Session()

    def close(self):
        """Call or remove method in the database"""
        DBStorage.__session.close()
