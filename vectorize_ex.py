from pymongo import MongoClient
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

client = MongoClient('localhost', 27017)
tokens = client['test-database']['test-collection'].find({})[100]['tokens']
stemmed_tokens = [porter.stem(t) for t in tokens]
stemmed_text = nltk.Text(stemmed_tokens)

stemmed_vectorizer = TfidfVectorizer()
X = stemmed_vectorizer.fit_transform(stemmed_text)
print(stemmed_vectorizer.get_feature_names_out())

# raw_text = nltk.Text(tokens)
# raw_vectorizer = TfidfVectorizer()
# X = raw_vectorizer.fit_transform(raw_text)
# print(raw_vectorizer.get_feature_names_out())