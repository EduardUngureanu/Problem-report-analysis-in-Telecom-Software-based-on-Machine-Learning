from typing import Collection
from pymongo import MongoClient
import nltk
import scipy.sparse
from sklearn.feature_extraction import DictVectorizer
import pprint
import utils

client = MongoClient('localhost', 27017)

def dict_vec(collection):
    list = []
    cursor = collection.find({})
    data = [ 'build', 'feature', 'release']
    for document in cursor:
        dict = {}
        for x in data:
            dict[x] = document[x]
            #dict comprehension
        list.append(dict)
    vec = DictVectorizer()
    x = vec.fit_transform(list)
    return x

#refactor variabile

def concat_and_save(collection):
    features_vec = dict_vec(collection)
    text_vec = utils.vectorize_all(collection)
    full_vec = scipy.sparse.hstack((features_vec, text_vec))
    scipy.sparse.save_npz('sparse_matrix.npz', full_vec)

concat_and_save(client['test-database']['test-collection'])
print("done")
# collection = client['test-database']['test-collection']
# scipy.sparse.save_npz('features.npz', dictVec(collection))
# scipy.sparse.save_npz('text.npz', utils.vectorize_all(collection))
# features = scipy.sparse.load_npz('features.npz')
# text = scipy.sparse.load_npz('text.npz')
# full_vec = scipy.sparse.hstack((features, text))
# print(full_vec)
# print(features.getformat())
# print(text.getformat())