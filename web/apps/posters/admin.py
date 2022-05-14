from django.contrib import admin

from apps.posters.models import TelegramChannel, InstagramProfile


@admin.register(TelegramChannel)
class TelegramChanelAdmin(admin.ModelAdmin):
    pass


@admin.register(InstagramProfile)
class InstragramProfileAdmin(admin.ModelAdmin):
    pass
