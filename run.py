import pickle_helper
import web_interface_utils
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

client = MongoClient('localhost', 27017)
collection = client['test-database']['test-collection']

pickle_helper.serialize_gaussian(collection)