from apps.posters.models import TelegramChannel, InstagramProfile, InstagrapiConfig
from django.contrib import admin


@admin.register(TelegramChannel)
class TelegramChanelAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramProfile)
class InstragramProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagrapiConfig)
class InstagrapiConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_post_date',)
