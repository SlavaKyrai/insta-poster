import praw
from django.conf import settings

reddit_client = praw.Reddit(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    user_agent='dj_imposter'
)
