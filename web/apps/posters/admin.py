from django.contrib import admin

from apps.posters.models import (
    TelegramChannel,
    InstagramProfile,
    InstagrapiConfig,
    InstagramHashtagFollowPromoteConfig,
    InstagramLikePromoteConfig,
    InstagramPostConfig
)


@admin.register(TelegramChannel)
class TelegramChanelAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramProfile)
class InstragramProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagrapiConfig)
class InstagrapiConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_post_date',)


@admin.register(InstagramPostConfig)
class InstagramPostConfigAdmin(admin.ModelAdmin):
    list_display = ('profile', 'is_enabled', 'last_post_date')


@admin.register(InstagramHashtagFollowPromoteConfig)
class InstagramHashtagFollowPromoteAdmin(admin.ModelAdmin):
    list_display = (
        'profile', 'is_enabled', 'promote_interval', 'follow_per_promotion',
        'get_rate_per_day', 'last_run_time'
    )

    def get_rate_per_day(self, obj):
        minutes_per_day = 24 * 60
        return int(minutes_per_day / obj.promote_interval * obj.follow_per_promotion)

    get_rate_per_day.short_description = 'Daily Rate'


@admin.register(InstagramLikePromoteConfig)
class InstagramLikePromoteAdmin(admin.ModelAdmin):
    list_display = (
        'profile', 'is_enabled', 'promote_interval', 'likes_per_promotion',
        'get_rate_per_day', 'last_run_time',
    )

    def get_rate_per_day(self, obj):
        minutes_per_day = 24 * 60
        return int(minutes_per_day / obj.promote_interval * obj.likes_per_promotion)

    get_rate_per_day.short_description = 'Daily Rate'
