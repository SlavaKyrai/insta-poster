import requests
from django.conf import settings
from telegram.ext import Updater

from apps.posters.models import TelegramChannel, InstagramProfile
from apps.posters.repositories import PosterService
from dj_imposter.celery import app


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
        post_publish_url = 'https://graph.facebook.com/v13.0/{}/media_publish'.format("17841410755264157")
        if post:
            try:
                payload = {
                    'image_url': post.image_url,
                    'caption': f'{post.title} {profile.hashtags}',
                    'access_token': profile.access_token
                }
                response = requests.post(post_media_url, data=payload)
                print('-'*50)
                print(response.json())
                print('-'*50)
                result = response.json()
                creation_id = result['id']
                second_payload = {
                    'creation_id': creation_id,
                    'access_token': profile.access_token
                }
                requests.post(post_publish_url, data=second_payload)
                print('-'*50)
                print(response.json())
                print('-'*50)
            except Exception as e:
                print(e)
            finally:
                post.is_instagram_posted = True
                post.save(update_fields={'is_instagram_posted'})
