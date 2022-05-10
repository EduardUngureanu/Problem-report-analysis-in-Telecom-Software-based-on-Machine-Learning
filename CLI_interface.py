import json
import scipy.sparse
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import nltk
from nltk import word_tokenize
from pymongo import MongoClient
import utils
import pickle_helper

def vectorize_all2(collection):
    twd = TreebankWordDetokenizer()
    list = []
    cursor = collection.find({})
    for document in cursor:
        text = TreebankWordDetokenizer.detokenize(twd, document['stemmedTokens'])
        list.append(text)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(list)
    return vectorizer

def features_vectorize2(collection):
    full_feature_list = []
    cursor = collection.find({})
    features_to_extract = ['build', 'feature', 'release']
    for document in cursor:
        feature_dict = {key:value for (key, value) in document.items() if key in features_to_extract}
        full_feature_list.append(feature_dict)
    vec = DictVectorizer()
    vec.fit(full_feature_list)
    return vec

def label_encode_gic2(collection):
    gic_list = []
    cursor = collection.find({})
    for document in cursor:
        gic_list.append(document['groupInCharge'])
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit_transform(gic_list)
    return label_encoder

def anylize_json():
    path = input("Please specify the path to the json file:\n")
    with open(path, 'r') as file:
        file_data = json.load(file)

    client = MongoClient('localhost', 27017)
    db = client['test-database']
    collection = db['test-collection']

    # if collection.count_documents({'problemReportId' : file_data['problemReportId']}) != 0:
    #     print("This problem report id already exists in the database.")
    #     return

    feature_vectorizer = pickle_helper.deserialize_dict_vec()
    features_to_extract = ['build', 'feature', 'release']
    feature_dict = {key:value for (key, value) in file_data.items() if key in features_to_extract}
    feature_matrix = feature_vectorizer.transform(feature_dict)

    text_vectorizer = pickle_helper.deserialize_tfidf_vec()
    porter = nltk.PorterStemmer()
    twd = TreebankWordDetokenizer()
    tokens = word_tokenize(file_data['title'] + ' ' + file_data['description'])
    stemmed_tokens = [porter.stem(t) for t in tokens]
    text = TreebankWordDetokenizer.detokenize(twd, stemmed_tokens)
    text_matrix = text_vectorizer.transform([text])

    full_matrix = scipy.sparse.hstack((feature_matrix, text_matrix))
    return full_matrix

def decode_gic(label):
    client = MongoClient('localhost', 27017)
    db = client['test-database']
    collection = db['test-collection']

    label_encoder = label_encode_gic2(collection)
    return(label_encoder.inverse_transform(label))

print(anylize_json())