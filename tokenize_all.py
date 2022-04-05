from pymongo import MongoClient
import nltk, re, pprint
from nltk import word_tokenize

client = MongoClient('localhost', 27017)
db = client['test-database']
collection = db['test-collection']

def tokenize_all(client : MongoClient):
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    for document in cursor:
        tokens = word_tokenize(document['description'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'tokens' : tokens}})

print(collection.find({})[100])