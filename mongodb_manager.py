import streamlit as st
from pymongo import DESCENDING
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from configurations import MONGO_DB_CONNECTION, MONGO_DB_DATABASE


@st.cache_resource
def init_connection():
    return MongoClient(MONGO_DB_CONNECTION, server_api=ServerApi('1'))


# Mongo DB Manager
class MongoDBManager:
    client = init_connection()
    db = client[MONGO_DB_DATABASE]

    def getData(self, table: str, uuid: str):
        Table = self.db[table]
        # Get One Data Point from Mongo
        user = Table.find_one({"uuid": uuid})
        return user

    def getAllData(self, table: str):
        Table = self.db[table]
        # Get All Data from Mongo
        collection = list(Table.find().sort("uploading_date", DESCENDING))
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
