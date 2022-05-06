import praw
from telegram.ext import Updater

reddit_client = praw.Reddit(client_id='cvME6Mm5pAU32g',
                     client_secret='QYqJgIWHAfsqCrKmOW7DFkpuuh8',
                     user_agent='dj_imposter')

if __name__ == '__main__':
    posts = reddit_client.subreddit('catpictures').top('day', limit=10)
    for post in posts:
        print(post.title)
        print(post.url)

        updater = Updater(
            token='5331800692:AAH2hSaVVAKavu7rqUtBt5jQHeawqT5tclo',
            use_context=True
        )
        result = updater.bot.send_photo(
            chat_id='-1001324657815',
            photo=post.url,
            caption=post.title
        )