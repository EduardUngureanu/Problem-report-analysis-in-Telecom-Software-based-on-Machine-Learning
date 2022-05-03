from typing import Collection
from pymongo import MongoClient
import nltk
import scipy.sparse
from sklearn.feature_extraction import DictVectorizer
import pprint
import utils

client = MongoClient('localhost', 27017)

# Extracts the desired features from the database and performs vectorization on them using DictVectorizer
def features_vectorize(collection):
    full_feature_list = []
    cursor = collection.find({})
    features_to_extract = ['build', 'feature', 'release']
    for document in cursor:
        feature_dict = {key:value for (key, value) in document.items() if key in features_to_extract}
        full_feature_list.append(feature_dict)
    print(full_feature_list)
    vec = DictVectorizer()
    sparse_matrix = vec.fit_transform(full_feature_list)
    return sparse_matrix

# Concatenate the vectorized feature list to the vectorized text and save them to a file called "sparse_matrix.npz"
def concat_and_save(collection):
    features_vec = features_vectorize(collection)
    text_vec = utils.vectorize_all(collection)
    full_vec = scipy.sparse.hstack((features_vec, text_vec))
    scipy.sparse.save_npz('sparse_matrix.npz', full_vec)

# concat_and_save(client['test-database']['test-collection'])
features_vectorize(client['test-database']['test-collection'])
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