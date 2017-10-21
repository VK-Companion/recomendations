import vk_api


def fetch_all_friends(vk_session, user_id):
    vk = vk_session.get_api()

    return vk.friends.get(user_id=user_id, count=5000, fields='sex,bdate,education')['items']


def fetch_all_friends_of_friends(vk_session, friends):
    user_vk_handles = dict()
    with vk_api.VkRequestsPool(vk_session) as pool:
        for friend in friends:
            friend_id = friend['id']
            user_vk_handles[friend_id] = pool.method('friends.get',
                                                     dict(user_id=friend_id, count=5000, fields='sex,bdate,education'))

    friends_of_friends = []
    for handle in user_vk_handles.values():
        if handle.ok:
            friends_of_friends.append(handle.result)

    return friends_of_friends
