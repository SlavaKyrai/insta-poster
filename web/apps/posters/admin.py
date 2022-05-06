from django.contrib import admin

from apps.posters.models import TelegramChannel


@admin.register(TelegramChannel)
class TelegramChanelAdmin(admin.ModelAdmin):
    pass
