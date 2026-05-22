import pymongo

from configurations import MONGO_DB_CONNECTION, MONGO_DB_DATABASE


# Mongo DB Manager
class MongoDBManager:
    client = pymongo.MongoClient(MONGO_DB_CONNECTION)
    db = client[MONGO_DB_DATABASE]

    def getData(self, table: str, uuid: str):
        Table = self.db[table]
        # Get One Data Point from Mongo
        user = Table.find_one({"uuid": uuid})
        return user

    def getAllData(self, table: str):
        Table = self.db[table]
        # Get All Data from Mongo
        collection = list(Table.find())
        return collection

    def addData(self, table: str, data: dict):
        Table = self.db[table]
        # Store Data in Mongo
        Table.insert_one(data)

    def updateData(self, table: str, uuid: str, data: dict):
        Table = self.db[table]
        # Update Data in Mongo
        Table.update_one({"uuid": uuid}, {"$set": data})

    def deleteData(self, table: str, uuid: str):
        Table = self.db[table]
        # Delete Data in Mongo
        Table.delete_one({"uuid": uuid})
