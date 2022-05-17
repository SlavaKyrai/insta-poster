from django.db import models

from apps.crawlers.models import RedditSource


class TelegramChannel(models.Model):
    name = models.CharField(max_length=50)
    chat_id = models.CharField(max_length=100)
    reddit_sources = models.ManyToManyField(RedditSource)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class InstagramProfile(models.Model):
    name = models.CharField(max_length=50)
    page_id = models.CharField(max_length=30)
    access_token = models.CharField(max_length=250)
    app_id = models.CharField(max_length=30)
    app_secret = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    reddit_sources = models.ManyToManyField(RedditSource)
    hashtags = models.TextField()

    def __str__(self):
        return self.name
