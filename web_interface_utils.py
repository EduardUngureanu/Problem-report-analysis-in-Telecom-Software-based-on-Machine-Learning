from random import gauss
import pickle_helper
import scipy.sparse
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk import word_tokenize
from sklearn.naive_bayes import GaussianNB

def parse_pronto_data(title, description, build, feature, release):
    text_vectorizer = pickle_helper.deserialize_tfidf_vec()
    porter = nltk.PorterStemmer()
    twd = TreebankWordDetokenizer()
    tokens = word_tokenize(title + ' ' + description)
    stemmed_tokens = [porter.stem(t) for t in tokens]
    text = TreebankWordDetokenizer.detokenize(twd, stemmed_tokens)
    text_matrix = text_vectorizer.transform([text])

    feature_vectorizer = pickle_helper.deserialize_dict_vec()
    feature_dict = {'build' : build, 'feature' : feature, 'release' : release}
    feature_matrix = feature_vectorizer.transform(feature_dict)

    data_matrix = scipy.sparse.hstack((feature_matrix, text_matrix))
    return data_matrix

def decode_gic(label):
    label_encoder = pickle_helper.deserialize_label_enc()
    return(label_encoder.inverse_transform(label))

def predict(data_matrix):
    gaussian = pickle_helper.deserialize_gaussian()
    label_result = gaussian.predict(data_matrix)
    return decode_gic(label_result)