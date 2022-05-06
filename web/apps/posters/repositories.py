from apps.crawlers.models import Post
from apps.posters.models import TelegramChannel


class TelegramPosterService:

    @staticmethod
    def get_post_for_telegram_upload(channel: TelegramChannel):
        post = Post.objects.filter(
            subreddit__in=channel.reddit_sources.filter(is_active=True),
            is_telegram_posted=False
        ).order_by('-score').first()
        return post