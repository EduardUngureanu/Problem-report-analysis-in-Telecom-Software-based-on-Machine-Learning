import pickle
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer

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
