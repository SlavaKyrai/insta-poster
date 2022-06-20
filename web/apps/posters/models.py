from django.contrib.postgres.fields import ArrayField
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


class InstagrapiConfig(models.Model):
    name = models.CharField(max_length=50, unique=True)
    comment_phrases = ArrayField(
        base_field=models.CharField(max_length=100),
    )
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    login_settings = models.JSONField()
    main_hashtag = models.CharField(max_length=50)
    posting_hashtags = models.TextField(null=True, blank=True)
    like_posts = models.BooleanField(default=True)
    follow_users = models.BooleanField(default=True)
    reddit_sources = models.ManyToManyField(RedditSource, blank=True)
    last_post_date = models.DateTimeField(null=True, blank=True)
    use_location_in_post = models.BooleanField(default=True)
    mention_author = models.BooleanField(default=False)

    def __str__(self):
        return self.name
