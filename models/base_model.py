#!/usr/bin/python3
'''
    This module establishes the BaseModel class.
'''
from os import getenv
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    '''
        Primary class serving as a foundation for other classes throughout its usage period
    '''
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        '''
            Create public instance attributes.
        '''
        if (len(kwargs) == 0):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("created_at"):
                kwargs["created_at"] = datetime.strptime(
                    kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("created_at"):
                kwargs["updated_at"] = datetime.strptime(
                    kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            for key, val in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, val)
            if not self.id:
                self.id = str(uuid.uuid4())

    def __str__(self):
        '''
            Provide string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dictt__))

    def __repr__(self):
        '''
            Provide the string representation of the BaseModel class.
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dictt__))

    def save(self):
        '''
            Upgrade the updated_at attribute with new.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dictt(self):
        '''
            Provide the dictionary representation of the BaseModel class
        '''
        cp_dctt = dict(self.__dictt__)
        cp_dctt['__class__'] = self.__class__.__name__
        cp_dctt['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dctt['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if hasattr(self, "_sa_instance_state"):
            del cp_dctt["_sa_instance_state"]
        return (cp_dctt)

    def delete(self):
        '''
            Removes an object
        '''
        models.storage.delete(self)
