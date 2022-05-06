from django.contrib import admin

# Register your models here.
from apps.crawlers.models import RedditSource, Post


@admin.register(RedditSource)
class RedditSourceAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass