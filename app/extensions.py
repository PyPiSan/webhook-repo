from pymongo import MongoClient
import os


# This is to connect to MongoDB database using Pymongo,
class MongoConnect:

    def __init__(self, data):
        conn_str = os.environ["CONN_STRING"] #MongoDB connection string stored in env
        self.client = MongoClient(conn_str)
        cursor = self.client.Webhook #collecting DB
        self.collection = cursor.gitresponse #collecting collection
        self.data = data

# Fetching data from dB, for(GET) method
    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'}
                  for data in documents] # escaping MongoDB default id at the response output
        return output

# Wrinting to dB, for (POST) method 
    def write(self, data):
        # log.info('Writing Data')
        new_document = data
        response = self.collection.insert_one(new_document) # using insert_one() method to inset data
        output = {'Status': 'Successfully Inserted'}
        return output
