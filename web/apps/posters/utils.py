import re
import tempfile
from contextlib import contextmanager
from math import cos, asin, sqrt
from pathlib import Path
from typing import Optional

import requests
import spacy
from geopy.geocoders import Nominatim
from instagrapi import Client
from instagrapi.types import User, Location

from apps.crawlers.models import Post
from apps.posters.dto import InstagramPostData
from apps.posters.models import InstagrapiConfig, InstagramPostConfig

# [OC] (OC) 1920x1800 variations
reddit_re = re.compile(
    r'(\[OC])|(\(OC\))|(\(\d+x\d+\))|(\[\d+x\d+\])|(\d+x\d+)',
    re.IGNORECASE
)


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
    is_logged = client.login(config.login, config.password, relogin=True)
    if not is_logged:
        client.relogin()
    return client


@contextmanager
def temp_file_from_url(url):
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(requests.get(url).content)
        tfile.flush()
        yield tfile.name


def normalize_title(title: str):
    normalized_title = reddit_re.sub('', title)
    title = " ".join(normalized_title.split())
    return title


def get_instagram_post_data(file_name: str, post: Post, config: InstagramPostConfig, client: Client):
    path = Path(file_name)
    title = normalize_title(post.title)
    caption = f'{title}\n.\n.\n.\n{config.posting_hashtags}'
    location = None
    if config.mention_author:
        if post.author:
            caption = f'{title}\n.\nauthor:{post.author} from reddit\n.\n.\n.\n{config.posting_hashtags}'
    if config.use_location_in_post:
        location = get_location_for_instagram(client, title)
    post_data = InstagramPostData(
        path=path,
        caption=caption,
        location=location
    )
    return post_data


def get_location_for_instagram(client: Client, text) -> Optional[Location]:
    try:
        text_location = get_location_name_from_text(text)
        if text_location:
            geolocation = get_geolocation_from_text(text_location)
            insta_locations = client.location_search(geolocation.latitude, geolocation.longitude)
            insta_locations.sort(
                key=lambda insta_loc: distance(
                    geolocation.latitude, geolocation.longitude, insta_loc.lat, insta_loc.lng
                )
            )
            for location in insta_locations:
                if get_location_name_from_text(location.name):
                    return location
    except Exception:
        return None
    return None


def get_geolocation_from_text(text):
    geolocator = Nominatim(user_agent='djimposter')
    geo_location = geolocator.geocode(text)
    return geo_location


def get_location_name_from_text(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ in ('GPE', 'LOC'):
            return str(entity)
    return None


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(hav))
