from pydoc import doc
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    f = open('descriptions', 'a')
    for document in cursor:
        f.write(document['description'])
        f.write('/r/n/r/n')