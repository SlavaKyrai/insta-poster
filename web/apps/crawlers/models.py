from django.db import models


class RedditSource(models.Model):
    subreddit_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    post_limit = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.subreddit_name


class Post(models.Model):
    subreddit = models.ForeignKey(RedditSource, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    title = models.TextField()
    image_url = models.URLField()
    score = models.BigIntegerField()
    hashtags = models.CharField(max_length=200, null=True, blank=True)
    is_telegram_posted = models.BooleanField(default=False)
    is_instagram_posted = models.BooleanField(default=False)

