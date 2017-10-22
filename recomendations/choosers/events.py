import numpy as np


def events_recomendations(vk_token, db_cache):
    user_lda = db_cache.get_user_lda(vk_token=vk_token)

    sugg = []
    for event in db_cache.get_events():
        event_lda = db_cache.get_event_lda(event_id=event['id'])
        r = np.dot(user_lda, event_lda)
        sugg.append((event, r))

    return sorted(sugg, key=lambda it: -it[1])