import pickle
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import scipy.sparse
import numpy
from sklearn.naive_bayes import GaussianNB
import utils

def serialize_tfidf_vec(collection, file_path = "tfidf_vec.out"):
    twd = TreebankWordDetokenizer()
    list = []
    cursor = collection.find({})
    for document in cursor:
        text = TreebankWordDetokenizer.detokenize(twd, document['stemmedTokens'])
        list.append(text)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(list)
    file = open(file_path, "w+b")
    pickle.dump(vectorizer, file)

def deserialize_tfidf_vec(file_path = "tfidf_vec.out"):
    file = open(file_path, "rb")
    return pickle.load(file)

def serialize_dict_vec(collection, file_path = "dict_vec.out"):
    full_feature_list = []
    cursor = collection.find({})
    features_to_extract = ['build', 'feature', 'release']
    for document in cursor:
        feature_dict = {key:value for (key, value) in document.items() if key in features_to_extract}
        full_feature_list.append(feature_dict)
    vectorizer = DictVectorizer()
    vectorizer.fit(full_feature_list)
    file = open(file_path, "w+b")
    pickle.dump(vectorizer, file)

def deserialize_dict_vec(file_path = "dict_vec.out"):
    file = open(file_path, "rb")
    return pickle.load(file)

def serialize_label_enc(collection, file_path = "label_enc.out"):
    gic_list = []
    cursor = collection.find({})
    for document in cursor:
        gic = document['groupInCharge'].split('_',1)[0]
        if (gic != 'MANO' or gic !='BOAM'):
            gic_list.append('not_boam')
        else:
            if gic == 'MANO':
                gic_list.append('BOAM')
            else:
                gic_list.append(gic)            
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(gic_list)
    file = open(file_path, "w+b")
    pickle.dump(label_encoder, file)

def deserialize_label_enc(file_path = "label_enc.out"):
    file = open(file_path, "rb")
    return pickle.load(file)

def serialize_gaussian(collection, file_path = "gaussian.out"):
    vectorized_features = scipy.sparse.load_npz('sparse_matrix.npz').toarray()
    vectorized_features = numpy.nan_to_num(vectorized_features, posinf=0.0, neginf=0.0)
    print("here")
    target = utils.label_encode_gic(collection)
    print("here")
    gaussian = GaussianNB()
    print("here")
    gaussian.fit(vectorized_features, target)
    print("here")
    file = open(file_path, "w+b")
    pickle.dump(gaussian, file)

def deserialize_gaussian(file_path = "gaussian.out"):
    file = open(file_path, "rb")
    return pickle.load(file)