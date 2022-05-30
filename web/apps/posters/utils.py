from instagrapi import Client
from instagrapi.types import User

from apps.posters.models import InstagrapiConfig


def is_valid_account_to_follow(user_info: User):
    if user_info.is_private:
        return False
    if user_info.following_count < 20:
        return False
    if user_info.follower_count < 20:
        return False
    if user_info.follower_count > 1500:
        return False
    following_rate = user_info.follower_count / user_info.following_count
    if following_rate < 0.15:
        return False
    if following_rate > 10:
        return False
    return True


def init_client(config: InstagrapiConfig) -> Client:
    client = Client()
    client.set_settings(config.login_settings)
    client.login(config.login, config.password)
    return client
