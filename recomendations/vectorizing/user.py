import datetime

import numpy as np

from recomendations.vectorizing.faculty_name import faculty_name_vector, load_default_faculty_name_vectorizers
from recomendations.vectorizing.subscriptions import load_default_subscription_vectorizers, subscriptions_vector

_education_count_vectorizer = None
_education_pca_vectorizer = None
_subscriptions_lda_vectorizer = None
_subscriptions_tfidf_vectorizer = None
_subscriptions_dictionary = None


def user_vector(user, subscriptions):
    arr = []
    arr.extend(_sex_user_vec_part(user))
    arr.extend(_bdate_user_vec_part(user))
    arr.extend(_education_user_vec_part(user))
    arr.extend(_subscriptions_user_vec_part(subscriptions))
    return np.array(arr)


def _sex_user_vec_part(user):
    return [int(user['sex']) == 1 if 'sex' in user else 0,
            int(user['sex']) == 2 if 'sex' in user else 0]


def _bdate_user_vec_part(user):
    if 'bdate' in user:
        bdate_parts = user['bdate'].split('.')
        bdate_year = bdate_parts[-1] if len(bdate_parts) == 3 else None
        current_year = datetime.datetime.now().year
        age = current_year - bdate_year
    else:
        age = None

    is_age_between_10_and_15 = int(10 <= age <= 15) if age is not None else 0
    is_age_between_16_and_20 = int(16 <= age <= 15) if age is not None else 0
    is_age_between_21_and_25 = int(21 <= age <= 25) if age is not None else 0
    is_age_between_26_and_30 = int(26 <= age <= 30) if age is not None else 0
    is_age_between_31_and_35 = int(31 <= age <= 35) if age is not None else 0
    is_age_between_36_and_inf = int(36 <= age) if age is not None else 0

    return [is_age_between_10_and_15, is_age_between_16_and_20, is_age_between_21_and_25,
            is_age_between_26_and_30, is_age_between_31_and_35, is_age_between_36_and_inf]


def _education_user_vec_part(user):
    global _education_count_vectorizer, _education_pca_vectorizer
    if _education_count_vectorizer is None and _education_pca_vectorizer is None:
        _education_count_vectorizer, _education_pca_vectorizer = load_default_faculty_name_vectorizers()

    return faculty_name_vector(user.get('university_name', ''), user.get('faculty_name', ''),
                               _education_count_vectorizer, _education_pca_vectorizer)


def _subscriptions_user_vec_part(subscriptions):
    global _subscriptions_lda_vectorizer, _subscriptions_tfidf_vectorizer, _subscriptions_dictionary
    if _subscriptions_lda_vectorizer is None and _subscriptions_tfidf_vectorizer is None and _subscriptions_dictionary is None:
        _subscriptions_lda_vectorizer, _subscriptions_tfidf_vectorizer, _subscriptions_dictionary = load_default_subscription_vectorizers()

    sub_descriptions = ['{} {}'.format(sub.get('name', ''), sub.get('description', '')) for sub in subscriptions]

    return subscriptions_vector(sub_descriptions,
                                _subscriptions_lda_vectorizer, _subscriptions_tfidf_vectorizer, _subscriptions_dictionary)
