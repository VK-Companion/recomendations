import pickle
from pathlib import Path

from pymongo import MongoClient


class DbCache:
    def __init__(self):
        self._events = None
        self._events_ldas = None

    def get_user_lda(self, vk_token):
        mongodb = MongoClient()
        collection = mongodb['user']
        data = collection.find_one({'vk_token': vk_token})
        return data['lda']

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
