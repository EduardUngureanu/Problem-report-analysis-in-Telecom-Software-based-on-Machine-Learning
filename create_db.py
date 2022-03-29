import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['test-database']
collection = db['test-collection']

with open('prontos.json') as file:
    file_data = json.load(file)

values_list = file_data['values']

collection.insert_many(values_list)

client.close()