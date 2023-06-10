from pymongo import MongoClient

import certifi

class AnimalShelter(object):
    def __init__(self):
        USER = "doadmin"
        PASS = "KoAq3251F409TiO7"
        HOST = "do340-be388ee0.mongo.ondigitalocean.com"
        PORT = 27017
        DB = "AAC"
        COL = "animals"

        self.client = MongoClient("mongodb+srv://" + USER + ":" + PASS + "@do340-be388ee0.mongo.ondigitalocean.com/"
                                                                             "admin?tls=true&authSource=admin&replicaSet=do340", tlsCAFile=certifi.where())
        self.database = self.client["%s" % (DB)]
        self.collection = self.database["%s" % (COL)]

# Create Class ----------------
    def Create(self, data):
        if data is not None:
            createstatus = self.database.animals.insert_one(data)
            return True if createstatus.acknowledged else False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Read Class ----------------
    def Read(self, search):
        # Create object of search results.
        items = list(self.database.animals.find(search, {"_id": False}))
        # iterate through the object

        return items

    def ReadAll(self):
        data = ""
        # Create object of search results.
        items = self.database.animals.find()
        # iterate through the object
        for item in items:
            item = str(item)
            data = data + item + " \n"
        # return a string of search results.
        return data

# Update Class ----------------
    def Update(self, search, update):
        update = {"$set": update}
        # update database
        x = self.database.animals.update_many(search, update)
        # return integer quantity of records modified
        return x.modified_count

# Delete Class ----------------
    def Delete(self, search):
        # Delete items from database
        x = self.database.animals.delete_many(search)
        # return integer quantity of records deleted
        return x.deleted_count
