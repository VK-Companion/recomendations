import vk_api
from tqdm import tqdm


def fetch_all_upcoming_events(vk_session, country_id, city_id):
    vk = vk_session.get_api()
    return vk.groups.search(q=' ', type='event', country_id=country_id, city_id=city_id, future=True, count=1000)['items']


def fetch_events_members(vk_session, events, verbose=False):
    vk = vk_session.get_api()
    tools = vk_api.VkTools(vk)

    members = dict()

    if verbose:
        events = tqdm(events)
    for event in events:
        event_members = tools.get_all('groups.getMembers', max_count=1000,
                                      values=dict(group_id=event['id']))['items']
        unsure_event_members = tools.get_all('groups.getMembers', max_count=1000,
                                             values=dict(group_id=event['id'], filter='unsure'))['items']

        members[event['id']] = dict()
        members[event['id']]['sure'] = event_members
        members[event['id']]['unsure'] = unsure_event_members

    return members


def fetch_events_walls(vk_session, events, verbose=False):
    vk = vk_session.get_api()

    texts = dict()

    if verbose:
        events = tqdm(events)
    for event in events:
        try:
            wall = vk.wall.get(owner_id=-int(event['id']), filter='owner', count=100)['items']
            texts[event['id']] = []
            for post in wall:
                texts[event['id']].append(post.get('text', ''))
                texts[event['id']].append(post.get('copy_history', [{}])[0].get('text', ''))
        except:
            pass

    return texts

