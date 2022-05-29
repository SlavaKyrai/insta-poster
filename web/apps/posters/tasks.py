import random
import time

import requests
from apps.posters.models import InstagrapiConfig
from apps.posters.models import TelegramChannel, InstagramProfile
from apps.posters.repositories import PosterService
from apps.posters.utils import is_valid_account_to_follow
from dj_imposter.celery import app
from django.conf import settings
from instagrapi import Client
from telegram.ext import Updater

insta_clients = {}


@app.task
def post_to_telegram_chats():
    for channel in TelegramChannel.objects.filter(is_active=True):
        post = PosterService.get_post_for_telegram_upload(channel)
        if post:
            try:
                updater = Updater(
                    token=settings.TELEGRAM_TOKEN_ID,
                    use_context=True
                )
                updater.bot.send_photo(
                    chat_id=channel.chat_id,
                    photo=post.image_url,
                    caption=post.title
                )
            except Exception as e:
                print(e)
            finally:
                post.is_telegram_posted = True
                post.save(update_fields={'is_telegram_posted'})


@app.task
def post_to_instagram_profile():
    for profile in InstagramProfile.objects.filter(is_active=True):
        post = PosterService.get_post_for_instagram_upload(profile)
        post_media_url = f'https://graph.facebook.com/v13.0/{profile.page_id}/media'
        post_publish_url = f'https://graph.facebook.com/v13.0/{profile.page_id}/media_publish'
        if post:
            payload = {
                'image_url': post.image_url,
                'caption': f'{post.title} {profile.hashtags}',
                'access_token': profile.access_token
            }
            try:
                response = requests.post(post_media_url, data=payload)
                result = response.json()
                creation_id = result['id']
                second_payload = {
                    'creation_id': creation_id,
                    'access_token': profile.access_token
                }
                requests.post(post_publish_url, data=second_payload)
            except Exception as e:
                print('-' * 50)
                print(post.image_url)
                print('-' * 50)
            finally:
                post.is_instagram_posted = True
                post.save(update_fields={'is_instagram_posted'})


@app.task
def init_clients():
    for config in InstagrapiConfig.objects.all():
        cl = Client()
        cl.set_settings(config.login_settings)
        cl.login(config.login, config.password)
        insta_clients[config.name] = cl


@app.task
def promote_insta_with_like_and_comment():
    for client_name, client in insta_clients.items():
        config = InstagrapiConfig.objects.get(name=client_name)
        medias = client.hashtag_medias_recent(config.main_hashtag, amount=30)
        for media in medias:
            try:
                if media.like_count > 700:
                    client.media_comment(random.choice(config.comment_phrases), media.id)
                else:
                    client.media_like(media.id)
            except Exception as e:
                print(e)
            else:
                time.sleep(random.randint(2, 7))


@app.task
def promote_insta_with_subscribe_like_and_comment():
    for client_name, client in insta_clients.items():
        config = InstagrapiConfig.objects.get(name=client_name)
        medias = client.hashtag_medias_recent(config.main_hashtag, amount=30)
        for media in medias:
            try:
                if media.like_count > 700:
                    client.media_comment(random.choice(config.comment_phrases), media.id)
                else:
                    client.media_like(media.id)
                    user_info = client.user_info(media.user.pk)
                    if is_valid_account_to_follow(user_info):
                        client.user_follow(user_info.pk)
            except Exception as e:
                print(e)
            else:
                time.sleep(random.randint(2, 10))
