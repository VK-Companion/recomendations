import pickle
from pathlib import Path

import pymorphy2
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore, TfidfModel
from nltk import ToktokTokenizer
from nltk.stem.snowball import SnowballStemmer

from recomendations.utils_nlp import get_stopwords

_alphabet = 'йцукенгшщзхъфывапролджэёячсмитьбю'
_morph = pymorphy2.analyzer.MorphAnalyzer()
_stemmer = SnowballStemmer('russian')
_stopwords = get_stopwords()


def subscriptions_vector(group_descriptions, lda_vectorizer, tfidf_vectorizer, dictionary):
    result = None
    for doc in group_descriptions:
        doc = _normalize_text(doc)
        doc = _tokenize_text(doc)
        doc = dictionary.doc2bow(doc)
        doc = tfidf_vectorizer[doc]
        doc = lda_vectorizer[doc]

        vec = [0] * 500
        for i, prob in doc:
            vec[i] = prob
        vec = np.array(vec)

        if result is None:
            result = vec
        else:
            result = result + vec
    return result


def create_subscription_vectorizers(group_descriptions):
    corpora_sentences = [_tokenize_text(_normalize_text(doc)) for doc in group_descriptions]

    dictionary = Dictionary(corpora_sentences)
    corpora_bow = [dictionary.doc2bow(doc) for doc in corpora_sentences]
    tfidf_vectorizer = TfidfModel(corpora_bow)
    corpora_tfidf = tfidf_vectorizer[corpora_bow]

    lda_vectorizer = LdaMulticore(num_topics=50, corpus=corpora_tfidf, id2word=dictionary)

    return lda_vectorizer, tfidf_vectorizer, dictionary


def load_default_subscription_vectorizers():
    root_path = Path(__file__).resolve().parent / '..' / '..' / 'resources' / 'subscriptions_vectorizers'
    lda_vectorizer_path = root_path / 'lda_vectorizer.pkl'
    tfidf_vectorizer_path = root_path / 'tfidf_vectorizer.pkl'
    dictionary_path = root_path / 'dictionary.pkl'

    with lda_vectorizer_path.open(mode='rb') as f:
        lda_vectorizer = pickle.load(f)
    with tfidf_vectorizer_path.open(mode='rb') as f:
        tfidf_vectorizer = pickle.load(f)
    with dictionary_path.open(mode='rb') as f:
        dictionary = pickle.load(f)

    return lda_vectorizer, tfidf_vectorizer, dictionary


def _normalize_text(s):
    s = s.lower()
    s = ''.join(c if c in _alphabet else ' ' for c in s)
    s = ' '.join(word for word in s.split(' ') if word not in _stopwords)
    s = ' '.join(_morph.parse(word)[0].normal_form for word in s.split(' ') if word != '')
    s = ' '.join(word for word in s.split(' ') if word not in _stopwords)
    s = ' '.join(_stemmer.stem(word) for word in s.split(' ') if word != '')
    s = ' '.join(word for word in s.split(' ') if word not in _stopwords)
    return s


def _tokenize_text(s):
    tokenizer = ToktokTokenizer()
    return tokenizer.tokenize(s)
