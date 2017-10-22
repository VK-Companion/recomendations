from pymongo import MongoClient


def get_vectorized_event_group(event_id):
    mongodb = MongoClient()
    collection = mongodb['events']
    data = collection.find_one({'_id': event_id})
    return data['lda']


class DbCache:
    raise NotImplementedError