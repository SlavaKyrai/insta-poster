import datetime
import logging

import requests
from django.conf import settings
from django.utils import timezone
from telegram.ext import Updater

from apps.posters.models import TelegramChannel, InstagramProfile, InstagrapiConfig, InstagramPostConfig
from apps.posters.repositories import PostRepository
from apps.posters.services import InstagramService
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
    """ POST to Instagram via LEGAL API"""
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
def post_photo_to_instagram():
    for client_config in InstagrapiConfig.objects.filter(post_photo=True):
        post = PostRepository.get_post_for_instagrapi_upload(client_config)
        if post:
            InstagramService(client_config).post_photo(post)


@app.task
def post_instagram_photo():
    for posting_config in InstagramPostConfig.objects.filter(is_enabled=True):
        post_time = timezone.now() - datetime.timedelta(minutes=posting_config.post_interval)
        if posting_config.last_post_date is None or posting_config.last_post_date < post_time:
            post = PostRepository.get_post_for_instagrapi_upload(posting_config.profile)
            if post:
                InstagramService(posting_config.profile).post_photo(post)
