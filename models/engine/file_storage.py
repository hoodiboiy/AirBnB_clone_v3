#!/usr/bin/python3
'''
    Declare the class FileStorage.
'''
import json
import models


class FileStorage:
    '''
        Serialize instances to a JSON file and perform deserialization from a JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Provide the dictionary
        '''
        new_dictt = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dictt[k] = v
            return new_dictt
        else:
            return self.__objects

    def new(self, objj):
        '''
            Assign the object with the key <object class name>.id to the __objects dictionary.
            Aguments:
                obj : An instance object.
        '''
        key = str(objj.__class__.__name__) + "." + str(objj.id)
        value_dict = objj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes the __objects attribute and stores the result in a JSON file.
        '''
        objects_dictt = {}
        for key, val in FileStorage.__objects.items():
            objects_dictt[key] = val.to_dictt()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dictt, fd)

    def reload(self):
        '''
            Deserializes the information from the JSON file and updates the __objects attribute.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_namee = val["__class__"]
                class_namee = models.classes[class_namee]
                FileStorage.__objects[key] = class_namee(**val)
        except FileNotFoundError:
            pass

    def delete(self, objj=None):
        '''
        Remove an object
        '''
        if objj is not None:
            key = str(objj.__class__.__name__) + "." + str(objj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        Convert the JSON file into objects through deserialization.
        '''
        self.reload()

    def get(self, cls, id):
        '''
        gets an object
        Args:
            cls (str): class name
            id (str): object ID
        Returns:
            an object based on class name and its ID
        '''
        objj_dictt = self.all(cls)
        for k, v in objj_dictt.items():
            matchstring = cls + '.' + id
            if k == matchstring:
                return v

        return None

    def count(self, cls=None):
        '''
        counts number of objects in a class (if given)
        Args:
            cls (str): class name
        Returns:
            number of objects in class, if no class name given
            return total number of objects in database
        '''
        objj_dictt = self.all(cls)
        return len(objj_dictt)
