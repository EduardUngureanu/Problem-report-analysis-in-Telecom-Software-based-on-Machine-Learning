from pymongo import MongoClient
import nltk

porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

client = MongoClient('localhost', 27017)
tokens = client['test-database']['test-collection'].find({})[100]['tokens']

print([porter.stem(t) for t in tokens][:30])
print([lancaster.stem(t) for t in tokens][:30])