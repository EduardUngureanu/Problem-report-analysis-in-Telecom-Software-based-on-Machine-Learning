import scipy.sparse
from curses import curs_set
from pydoc import doc
from typing import Collection
import numpy

import nltk
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from pymongo import MongoClient
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# Tokenize the descriptions and save them to the database
def tokenize_desc(client : MongoClient):
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    for document in cursor:
        tokens = word_tokenize(document['description'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'tokens' : tokens}})

# Conacatenate the title and description, tokenize them and save them to the database
def tokenize_full(collection):
    cursor = collection.find({})
    for document in cursor:
        tokens = word_tokenize(document['title'] + ' ' + document['description'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'tokens' : tokens}})

# Perform stemming on the tokens saved in the database and save the stemmed tokens back to the database
def stemm_full(collection, stemmer):
    cursor = collection.find({})
    for document in cursor:
        stemmed_tokens = [stemmer.stem(t) for t in document['tokens']]
        collection.update_one({'_id' : document['_id']}, {'$set' : {'stemmedTokens' : stemmed_tokens}})

# Not working
def stemm_to_text(collection):
    cursor = collection.find({})
    for document in cursor:
        stemmed_text = nltk.Text(document['stemmedTokens'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'stemmedText' : stemmed_text}})

# Turn the stemmed tokens from the database back into text and perform TFIDF vectorization on them
def vectorize_all(collection):
    twd = TreebankWordDetokenizer()
    list = []
    cursor = collection.find({})
    for document in cursor:
        text = TreebankWordDetokenizer.detokenize(twd, document['stemmedTokens'])
        list.append(text)
    vectorizer = TfidfVectorizer()
    sparse_matrix = vectorizer.fit_transform(list)
    return sparse_matrix

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
    text_vec = vectorize_all(collection)
    full_vec = scipy.sparse.hstack((features_vec, text_vec))
    scipy.sparse.save_npz('sparse_matrix.npz', full_vec)

# Encode the categorical groups in charge into labels
def label_encode_gic(collection):
    gic_dict = {}
    gic_list = []
    cursor = collection.find({})
    for document in cursor:
        gic = document['groupInCharge'].split('_',1)[0]
        if (gic != 'MOAM' or gic !='BOAM'):
            gic_list.append('not_boam')
        else:
            if gic == 'MOAN':
                gic_list.append('BOAM')
            else:
                gic_list.append(gic)            
    label_encoder = preprocessing.LabelEncoder()
    encoded_gic = label_encoder.fit_transform(gic_list)
    return encoded_gic

def gaussian_ml():
    vectorized_features = scipy.sparse.load_npz('sparse_matrix.npz').toarray()
    vectorized_features = numpy.nan_to_num(vectorized_features, posinf=0.0, neginf=0.0)
    target = label_encode_gic(client['test-database']['test-collection'])
    vf_train, vf_test, target_train, target_test = train_test_split(vectorized_features, target)
    gnb = GaussianNB()
    target_pred = gnb.fit(vf_train,target_train).predict(vf_test)
    print("Number of mislabeled points out of a total %d points : %d" % (vf_test.shape[0], (target_test != target_pred).sum()))

client = MongoClient('localhost', 27017)

if __name__ == "__main__":
    gaussian_ml()
    #print(len(label_encode_gic(client['test-database']['test-collection'])))

# stemm_to_text(client['test-database']['test-collection'])
# text = nltk.Text(client['test-database']['test-collection'].find_one({})['stemmedTokens'])
# tokens = client['test-database']['test-collection'].find_one({})['tokens']
# print(TreebankWordDetokenizer.detokenize(TreebankWordDetokenizer(), tokens))
# vectorize_all(client['test-database']['test-collection'])
# print(label_encode_gic(client['test-database']['test-collection']))
