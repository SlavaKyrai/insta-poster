from django.db import models

from apps.crawlers.models import RedditSource


class TelegramChannel(models.Model):
    name = models.CharField(max_length=50)
    chat_id = models.CharField(max_length=100)
    reddit_sources = models.ManyToManyField(RedditSource)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
