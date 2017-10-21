import vk_api


def fetch_all_upcoming_events(vk_session, country_id, city_id):
    vk = vk_session.get_api()

    tools = vk_api.VkTools(vk)
    return tools.get_all('groups.search', max_count=1000,
                         values=dict(q=' ', type='event', country_id=country_id, city_id=city_id, future=True))['items']
