from pymongo import MongoClient
import nltk
import scipy.sparse
from sklearn.feature_extraction import DictVectorizer
import pprint
import utils

client = MongoClient('localhost', 27017)

def dictVec(collection):
    list = []
    cursor = collection.find({})
    data = ['author', 'build', 'feature', 'authorGroup', 'release']
    for document in cursor:
        dict = {}
        for x in data:
            dict[x] = document[x]
        list.append(dict)
    vec = DictVectorizer()
    x = vec.fit_transform(list)
    return x

def concat_and_save(collection):
    features_vec = dictVec(collection)
    text_vec = utils.vectorize_all(collection)
    full_vec = scipy.sparse.hstack(features_vec, text_vec)
    scipy.sparse.save_npz('sparse_matrix.npz', full_vec)

concat_and_save(client['test-database']['test-collection'])