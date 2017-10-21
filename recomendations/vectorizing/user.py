import datetime

import numpy as np

from recomendations.vectorizing.faculty_name import faculty_name_vector, load_default_faculty_name_vectorizers

_count_vectorizer = None
_pca_vectorizer = None


def user_vector(user):
    arr = []
    arr.extend(_sex_user_vec_part(user))
    arr.extend(_bdate_user_vec_part(user))
    arr.extend(_education_user_vec_part(user))

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

    is_age_between_10_and_15_prob = int(10 <= age <= 15) if age is not None else 0
    is_age_between_16_and_20_prob = int(16 <= age <= 15) if age is not None else 0
    is_age_between_21_and_25_prob = int(21 <= age <= 25) if age is not None else 0
    is_age_between_26_and_30_prob = int(26 <= age <= 30) if age is not None else 0
    is_age_between_31_and_35_prob = int(31 <= age <= 35) if age is not None else 0
    is_age_between_36_and_inf_prob = int(36 <= age) if age is not None else 0

    return [is_age_between_10_and_15_prob, is_age_between_16_and_20_prob, is_age_between_21_and_25_prob,
            is_age_between_26_and_30_prob, is_age_between_31_and_35_prob, is_age_between_36_and_inf_prob]

def _education_user_vec_part(user):
    global _count_vectorizer, _pca_vectorizer
    if _count_vectorizer is None and _pca_vectorizer is None:
        _count_vectorizer, _pca_vectorizer = load_default_faculty_name_vectorizers()

    return faculty_name_vector(user.get('university_name', ''), user.get('faculty_name', ''),
                               _count_vectorizer, _pca_vectorizer)
