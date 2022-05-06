from apps.posters.models import TelegramChannel
from dj_imposter.celery import app
from django.conf import settings
from telegram.ext import Updater

from apps.posters.repositories import TelegramPosterService


@app.task
def post_to_telegram_chats():
    for channel in TelegramChannel.objects.filter(is_active=True):
        print('channel')
        post = TelegramPosterService.get_post_for_telegram_upload(channel)
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
                #TODO: add logger
                print(e)
            finally:
                post.is_telegram_posted = True
                post.save(update_fields={'is_telegram_posted'})

