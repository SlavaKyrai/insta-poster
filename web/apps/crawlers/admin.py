from django.contrib import admin

# Register your models here.
from apps.crawlers.models import RedditSource, Post


@admin.register(RedditSource)
class RedditSourceAdmin(admin.ModelAdmin):
    list_display = ('subreddit_name', 'is_active', 'post_limit')
    list_filter = ('is_active',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('subreddit',)
    list_display = ('get_subreddit', 'is_telegram_posted', 'is_instagram_posted')

    def get_subreddit(self, obj):
        return obj.subreddit.subreddit_name

    get_subreddit.short_description = get_subreddit
