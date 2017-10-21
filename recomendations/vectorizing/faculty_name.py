import pickle
from pathlib import Path

import pymorphy2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from tqdm import tqdm

_morph = pymorphy2.analyzer.MorphAnalyzer()
_alphabet = 'йцукенгшщзхъфывапролджэёячсмитьбю'
_stopwords = {'факультет', 'институт', 'бывш', 'кафедра', 'школа', 'высокий', 'имя', 'при'}


def faculty_name_vector(university_name, faculty_name, count_vectorizer, pca_vectorizer):
    normalized_faculty_name = _normalize_faculty_name('{} - {}'.format(university_name, faculty_name))
    count_vec = count_vectorizer.transform([normalized_faculty_name]).toarray()
    pca_vec = pca_vectorizer.transform(count_vec)
    return pca_vec


def fetch_all_faculties_names(vk_session, verbose=False):
    vk = vk_session.get_api()

    cities = vk.database.getCities(country_id=1, count=1000)['items']

    universities = []
    if verbose:
        cities = tqdm(cities, 'cities')
    for city in cities:
        city_universities = vk.database.getUniversities(country_id=1, city_id=city['id'], count=10000)['items']
        universities.extend(city_universities)

    faculty_names = []
    if verbose:
        universities = tqdm(universities, 'universities')
    for university in universities:
        university_faculties = vk.database.getFaculties(university_id=university['id'], count=10000)['items']
        faculty_names.extend(['{} - {}'.format(university['title'], fac['title']) for fac in university_faculties])

    return faculty_names


def create_faculty_name_vectorizers(faculty_names):
    transformed_names = [_normalize_faculty_name(fac) for fac in faculty_names]

    count_vectorizer = CountVectorizer()
    counted_names = count_vectorizer.fit_transform(transformed_names).toarray()

    pca_vectorizer = PCA(n_components=50)
    pca_vectorizer.fit(counted_names)

    return count_vectorizer, pca_vectorizer


def load_default_faculty_name_vectorizers():
    root_path = Path(__file__).resolve().parent / '..' / '..' / 'resources' / 'faculty_name_vectorizers'
    count_vectorizer_path = root_path / 'count_vectorizer.pkl'
    pca_vectorizer_path = root_path / 'pca_vectorizer.pkl'

    with count_vectorizer_path.open(mode='rb') as f:
        count_vectorizer = pickle.load(f)
    with pca_vectorizer_path.open(mode='rb') as f:
        pca_vectorizer = pickle.load(f)

    return count_vectorizer, pca_vectorizer


def _normalize_faculty_name(s):
    s = s.lower()
    s = ''.join([c if c in _alphabet else ' ' for c in s])
    s = ' '.join(word for word in s.split(' ') if len(word) >= 3)
    s = ' '.join(_morph.parse(word)[0].normal_form for word in s.split(' ') if word != '')
    s = ' '.join(word for word in s.split(' ') if word not in _stopwords)
    return s
