from flask import Flask
import numpy as np

from recomendations.web.db import DbCache
from recomendations.choosers.events import events_recomendations as events_recomendations_chooser

app = Flask(__name__)
db_cache = DbCache()


@app.route('/events_recomendations/<vk_token>')
def events_recomendations(vk_token):
    events_ratings = events_recomendations_chooser(vk_token, db_cache)
    es = []
    for it in events_ratings:
        e = it[0]
        e['rating'] = it[1]
        es.append(e)
    return {'items': es}


@app.route('/companion_recomendations/<vk_token>/<event_id>')
def companion_recomendations(vk_token, event_id):
    user_lda = db_cache.get_user_lda(vk_token=vk_token)

    sugg = []
    for event in db_cache.get_events():
        event_lda = db_cache.get_event_lda(event_id=event['id'])
        r = np.dot(user_lda, event_lda)
        sugg.append((event['id'], r))

    return sorted(sugg, key=lambda it: -it[1])


@app.route('/register/<vk_token>')
def register(vk_token):
    db_cache.new_user(vk_token)
    return {'ok': True}


@app.route('/register_progress/<vk_token>')
def register_progress(vk_token):
    return {'done': db_cache.get_user_progress(vk_token)}


