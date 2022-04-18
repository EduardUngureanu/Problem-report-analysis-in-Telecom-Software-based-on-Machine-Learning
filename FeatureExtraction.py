from pymongo import MongoClient
import nltk
from sklearn.feature_extraction import DictVectorizer
import pprint

client = MongoClient('localhost', 27017)

def dictVec(client):
    list = []
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    data = ['author', 'build', 'feature', 'authorGroup', 'release']
    for document in cursor:
        dict = {}
        for x in data:
            dict[x] = document[x]
        list.append(dict)
    vec = DictVectorizer()
    x = vec.fit_transform(list)
    print(vec.get_feature_names())
    return vec

x = dictVec(client)
x.get_feature_names_out()