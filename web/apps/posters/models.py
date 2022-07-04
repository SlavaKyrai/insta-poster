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
    post_photo = models.BooleanField(default=True)
    last_post_date = models.DateTimeField(null=True, blank=True)
    use_location_in_post = models.BooleanField(default=True)
    mention_author = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class InstagramPostConfig(models.Model):
    profile = models.OneToOneField(
        InstagrapiConfig,
        on_delete=models.CASCADE,
        related_name='postconfig'
    )
    is_enabled = models.BooleanField(default=True)
    posting_hashtags = models.TextField(null=True, blank=True)
    reddit_sources = models.ManyToManyField(RedditSource, blank=True)
    mention_author = models.BooleanField(default=True)
    post_interval = models.PositiveIntegerField(
        default=360,
        help_text='Run post every N minutes'
    )
    use_location_in_post = models.BooleanField(default=True)
    last_post_date = models.DateTimeField(null=True, blank=True)


class InstagramLikePromoteConfig(models.Model):
    profile = models.OneToOneField(
        InstagrapiConfig,
        on_delete=models.CASCADE,
        related_name='likeconfig'
    )
    hashtag = models.CharField(
        max_length=50,
        help_text='Search posts and authors with this hashtag',
        null=True,
        blank=True
    )
    is_enabled = models.BooleanField(default=True)
    promote_interval = models.PositiveIntegerField(
        default=180,
        help_text='Run likes promotion every N minutes'
    )
    likes_per_promotion = models.PositiveIntegerField(
        default=20,
        help_text='Count of likes for 1 Promotion task'
    )
    last_run_time = models.DateTimeField(null=True, blank=True)


class InstagramHashtagFollowPromoteConfig(models.Model):
    profile = models.OneToOneField(
        InstagrapiConfig,
        on_delete=models.CASCADE,
        related_name='followconfig'
    )
    is_enabled = models.BooleanField(default=True)
    hashtag = models.CharField(
        max_length=50,
        help_text='Search posts and authors with this hashtag'
    )
    promote_interval = models.PositiveIntegerField(
        default=180,
        help_text='Run follow promotion every N minutes'
    )
    follow_per_promotion = models.PositiveIntegerField(
        default=10,
        help_text='Count of follow for 1 Promotion task'
    )
    last_run_time = models.DateTimeField(null=True, blank=True)
