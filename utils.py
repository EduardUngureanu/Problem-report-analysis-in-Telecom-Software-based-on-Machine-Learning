from curses import curs_set
from pydoc import doc
from typing import Collection
from pymongo import MongoClient
import nltk
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

def tokenize_desc(client : MongoClient):
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    for document in cursor:
        tokens = word_tokenize(document['description'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'tokens' : tokens}})

def tokenize_full(client : MongoClient):
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    for document in cursor:
        tokens = word_tokenize(document['title'] + ' ' + document['description'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'tokens' : tokens}})

def stemm_full(collection, stemmer):
    cursor = collection.find({})
    for document in cursor:
        stemmed_tokens = [stemmer.stem(t) for t in document['tokens']]
        collection.update_one({'_id' : document['_id']}, {'$set' : {'stemmedTokens' : stemmed_tokens}})

def stemm_to_text(collection):
    cursor = collection.find({})
    for document in cursor:
        stemmed_text = nltk.Text(document['stemmedTokens'])
        collection.update_one({'_id' : document['_id']}, {'$set' : {'stemmedText' : stemmed_text}})

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

def label_encode_gic(collection):
    gic_list = []
    cursor = collection.find({})
    for document in cursor:
        gic_list.append(document['groupInCharge'])
    le = preprocessing.LabelEncoder()
    encoded_gic = le.fit_transform(gic_list)
    return encoded_gic

client = MongoClient('localhost', 27017)
# stemm_to_text(client['test-database']['test-collection'])
# text = nltk.Text(client['test-database']['test-collection'].find_one({})['stemmedTokens'])
# tokens = client['test-database']['test-collection'].find_one({})['tokens']
# print(TreebankWordDetokenizer.detokenize(TreebankWordDetokenizer(), tokens))
# vectorize_all(client['test-database']['test-collection'])
print(label_encode_gic(client['test-database']['test-collection']))