from apps.crawlers.crawlers.reddit import reddit_client
from apps.crawlers.models import Post, RedditSource
from dj_imposter.celery import app


@app.task
def crawl_reddit_post():
    for source in RedditSource.objects.filter(is_active=True):
        posts = reddit_client.subreddit(source.subreddit_name).top('week', limit=source.post_limit)
        for post in posts:
            Post.objects.update_or_create(
                id=post.id,
                defaults={
                    'title': post.title,
                    'image_url': post.url,
                    'score': post.score,
                    'subreddit': source,
                    'author': post.author
                }
            )
