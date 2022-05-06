from django.conf import settings
from telegram.ext import Updater

from apps.crawlers.models import Post
from apps.posters.models import TelegramChannel
from dj_imposter.celery import app


@app.task
def post_to_telegram_chats():
    for channel in TelegramChannel.objects.filter(is_active=True):
        post = Post.objects.filter(
            subreddit__in=channel.reddit_sources.filter(is_active=True),
            is_telegram_posted=False
        ).order_by('-score').first()
        if post:
            updater = Updater(
                token=settings.TELEGRAM_TOKEN_ID,
                use_context=True
            )
            updater.bot.send_photo(
                chat_id=channel.chat_id,
                photo=post.image_url,
                caption=post.title
            )
            post.is_telegram_posted = True
            post.save(update_fields={'is_telegram_posted'})
