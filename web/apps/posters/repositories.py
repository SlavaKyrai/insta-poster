from apps.crawlers.models import Post
from apps.posters.models import TelegramChannel, InstagramProfile, InstagrapiConfig


class PostRepository:

    @staticmethod
    def get_post_for_telegram_upload(channel: TelegramChannel):
        post = Post.objects.filter(
            subreddit__in=channel.reddit_sources.filter(is_active=True),
            is_telegram_posted=False
        ).order_by('-score').first()
        return post

    @staticmethod
    def get_post_for_instagram_upload(profile: InstagramProfile):
        post = Post.objects.filter(
            subreddit__in=profile.reddit_sources.filter(is_active=True),
            is_instagram_posted=False
        ).order_by('-score').first()
        return post

    @staticmethod
    def get_post_for_instagrapi_upload(config: InstagrapiConfig):
        post = Post.objects.filter(
            subreddit__in=config.reddit_sources.filter(is_active=True),
            is_instagram_posted=False
        ).order_by('-score').first()
        return post
