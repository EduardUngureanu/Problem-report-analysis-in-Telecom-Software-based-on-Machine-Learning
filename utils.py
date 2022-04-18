from pydoc import doc
from pymongo import MongoClient
import nltk
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

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

def vectorize_all(client : MongoClient):
    porter = nltk.PorterStemmer()
    db = client['test-database']
    collection = db['test-collection']
    cursor = collection.find({})
    for document in cursor:
        tokens = document['tokens']
        stemmed_tokens = [porter.stem(t) for t in tokens]
        stemmed_text = nltk.Text(stemmed_tokens)
        stemmed_vectorizer = TfidfVectorizer()
        X = stemmed_vectorizer.fit_transform(stemmed_text)
        collection.update_one({'_id' : document['_id']}, {'$set' : {'TfidVector' : stemmed_vectorizer}})

client = MongoClient('localhost', 27017)
vectorize_all(client)
print(client['test-database']['test-collection'].find_one({})['TfidVector'])