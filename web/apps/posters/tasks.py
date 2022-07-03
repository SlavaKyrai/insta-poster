import logging
import random
import time

import requests
from django.conf import settings
from telegram.ext import Updater

from apps.posters.models import InstagrapiConfig
from apps.posters.models import TelegramChannel, InstagramProfile
from apps.posters.repositories import PostRepository
from apps.posters.services import InstagramService
from apps.posters.utils import init_client
from apps.posters.utils import is_valid_account_to_follow
from dj_imposter.celery import app

logger = logging.getLogger('celery')


@app.task
def post_to_telegram_chats():
    for channel in TelegramChannel.objects.filter(is_active=True):
        post = PostRepository.get_post_for_telegram_upload(channel)
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
                logger.error(f'Failed to post to telegram {channel.name} details: {e}')
            finally:
                post.is_telegram_posted = True
                post.save(update_fields={'is_telegram_posted'})


@app.task
def post_to_instagram_profile():
    for profile in InstagramProfile.objects.filter(is_active=True):
        post = PostRepository.get_post_for_instagram_upload(profile)
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
                logger.error(
                    f'Failed to post to telegram {profile.name} url {post.image_url} details: {e}'
                )
            finally:
                post.is_instagram_posted = True
                post.save(update_fields={'is_instagram_posted'})


@app.task
def promote_insta_by_like():
    for client_config in InstagrapiConfig.objects.filter(like_posts=True):
        client = init_client(client_config)
        medias = client.hashtag_medias_recent(client_config.main_hashtag, amount=30)
        for media in medias:
            try:
                client.media_like(media.id)
            except Exception as e:
                logger.error(
                    f'Failed to promote insta {client_config.name} details: {e}'
                )
            else:
                time.sleep(random.randint(3, 10))


@app.task
def promote_insta_by_subscribe():
    for client_config in InstagrapiConfig.objects.filter(follow_users=True):
        client = init_client(client_config)
        medias = client.hashtag_medias_recent(client_config.main_hashtag, amount=30)
        for media in medias:
            try:
                client.media_like(media.id)
                user_info = client.user_info(media.user.pk)
                if is_valid_account_to_follow(user_info):
                    client.user_follow(user_info.pk)
            except Exception as e:
                logger.error(
                    f'Failed to promote insta {client_config.name} details: {e}'
                )
            else:
                time.sleep(random.randint(2, 15))


@app.task
def post_photo_to_instagram():
    for client_config in InstagrapiConfig.objects.filter(post_photo=True):
        post = PostRepository.get_post_for_instagrapi_upload(client_config)
        if post:
            InstagramService(client_config).post_photo(post)
