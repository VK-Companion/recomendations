from flask import Flask
import numpy as np

from recomendations.web.db import DbCache

app = Flask(__name__)
db_cache = DbCache()


@app.route('/event_recomendations/<vk_token>')
def event_recomendations(vk_token):
    user_lda = db_cache.get_user_lda(vk_token=vk_token)

    sugg = []
    for event in db_cache.get_events():
        event_lda = db_cache.get_event_lda(event_id=event['id'])
        r = np.dot(user_lda, event_lda)
        sugg.append((event['id'], r))

    return sorted(sugg, key=lambda it: -it[1])


@app.route('/companion_recomendations/<vk_token>/<event_id>')
def companion_recomendations(vk_token, event_id):
    raise NotImplementedError


@app.route('/register', methods=['POST'])
def register():
    raise NotImplementedError


@app.route('/register_progress')
def register_progress():
    raise NotImplementedError


