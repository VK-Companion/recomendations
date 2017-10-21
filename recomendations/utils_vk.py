import os

import vk_api


def get_vk_session():
    token = os.getenv('VK_TOKEN')
    return vk_api.VkApi(token=token)