import praw
from django.conf import settings

from apps.crawlers.models import Post

reddit_client = praw.Reddit(client_id=settings.CLIENT_ID,
                     client_secret=settings.CLIENT_SECRET,
                     user_agent='dj_imposter')

if __name__ == '__main__':
    posts = reddit_client.subreddit('catpictures').top('day', limit=10)
    for post in posts:
        print(post.title)
        print(post.url)

