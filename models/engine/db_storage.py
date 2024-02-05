#!/usr/bin/python3
'''
    Declare the class DatabaseStorage.
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
        Establish SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Establish an engine and establish a connection to the MySQL database (hbnb_dev, hbnb_dev_db).
        '''
        user = getenvv("HBNB_MYSQL_USER")
        pwd = getenvv("HBNB_MYSQL_PWD")
        host = getenvv("HBNB_MYSQL_HOST")
        db = getenvv("HBNB_MYSQL_DB")
        envv = getenvv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            Retrieve information from the current database session
        '''
        db_dictt = {}

        if cls is not None and cls != '':
            objs = self.__session.query(models.classes[cls]).all()
            for objj in objs:
                key = "{}.{}".format(objj.__class__.__name__, objj.id)
                db_dictt[key] = objj
            return db_dictt
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for objj in objs:
                            key = "{}.{}".format(objj.__class__.__name__,
                                                 objj.id)
                            db_dictt[key] = objj
            return db_dictt

    def new(self, obtj):
        '''
            Include the object in the current database session
        '''
        self.__session.add(obtj)

    def save(self):
        '''
            Commit all changes made in the present database session.
        '''
        self.__session.commit()

    def delete(self, objj=None):
        '''
            Delete from current database session
        '''
        if objj is not None:
            self.__session.delete(objj)

    def reload(self):
        '''
            Persist all modifications made in the current database session
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Delete private session attribute
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
        Retrieves an object
        Args:
            cls (str): class name
            id (str): object ID
        Returns:
            Instantiate an object using its class name and corresponding ID
        '''
        objj_dictt = models.storage.all(cls)
        for k, v in objj_dictt.items():
            matchstring = cls + '.' + id
            if k == matchstring:
                return v

        return None

    def count(self, cls=None):
        '''
        Determines the count of objects belonging to a specific class, if provided.
        Args:
            cls (str): class name
        Returns:
            Returns the total number of objects in a specified class
            if no class name is provided, it retrieves the overall count of objects in the database.
        '''
        objj_dictt = models.storage.all(cls)
        return len(objj_dictt)
