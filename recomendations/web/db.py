import pickle
from multiprocessing.pool import Pool
from pathlib import Path
import numpy as np

import vk_api
from pymongo import MongoClient

from recomendations.fetchers.users import fetch_subscriptions
from recomendations.vectorizing.user import _subscriptions_user_vec_part


class DbCache:
    def __init__(self):
        self._events = None
        self._events_ldas = None

    def get_user_lda(self, vk_token):
        mongodb = MongoClient()
        collection = mongodb['users']
        data = collection.find_one({'vk_token': vk_token})
        return np.array(data['lda'])

    def get_events(self):
        if self._events is None:
            path = Path(__file__).resolve().parent / '..' / '..' / 'resources' / 'events' / 'events.pkl'
            with path.open(mode='rb') as f:
                self._events = pickle.load(f)
        return self._events

    def get_event_lda(self, event_id):
        if self._events_ldas is None:
            path = Path(__file__).resolve().parent / '..' / '..' / 'resources' / 'events' / 'event_ldas.pkl'
            with path.open(mode='rb') as f:
                self.events_ldas = pickle.load(f)
        return self._events_ldas[event_id]

    def new_user(self, vk_token):
        vk = vk_api.VkApi(token=vk_token).get_api()
        user = vk.users.get(fields='sex,bdate,education')[0]

        mongodb = MongoClient()
        collection = mongodb['users']
        collection.insert_one({
            '_id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'sex': user['sex'],
            'bdate': user['bdate'],
            'education': user['education'],
            'done': False
        })

        pool = Pool(processes=1)
        pool.apply_async(_new_user_job, args=(vk_token, user['id']))

    def get_user_progress(self, vk_token):
        mongodb = MongoClient()
        collection = mongodb['users']
        data = collection.find_one({'vk_token': vk_token})
        return data['done']


def _new_user_job(vk_token, user_id):
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    subs = fetch_subscriptions(vk_session, user_id)
    lda = list(_subscriptions_user_vec_part(subs))

    mongodb = MongoClient()
    collection = mongodb['users']
    collection.update_one({ '_id': user_id, },
                          {'$set': {
                              'subscriptions': subs,
                              'lda': lda,
                              'done': True
                          }})
