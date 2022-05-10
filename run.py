import pickle_helper
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

client = MongoClient('localhost', 27017)
collection = client['test-database']['test-collection']

pickle_helper.serialize_dict_vec(collection)