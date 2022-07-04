import datetime
import logging

import celery
from django.utils import timezone

from apps.posters.models import InstagramLikePromoteConfig, InstagramHashtagFollowPromoteConfig
from apps.posters.tasks.promotion import promote_instagram_by_like, promote_instagram_by_following
from dj_imposter.celery import app

logger = logging.getLogger('celery')


@app.task
def run_likes_by_hashtag_promotion_campaigns():
    for promo_config in InstagramLikePromoteConfig.objects.filter(is_enabled=True):
        last_promo_time = timezone.now() - datetime.timedelta(minutes=promo_config.promote_interval)
        promo_tasks = []
        if promo_config.last_run_time is None or promo_config.last_run_time < last_promo_time:
            promo_tasks.append(
                promote_instagram_by_like.s(promo_config.id)
            )
        celery.group(promo_tasks).apply_async()


@app.task
def run_follow_by_hashtag_promotion_campaigns():
    for promo_config in InstagramHashtagFollowPromoteConfig.objects.filter(is_enabled=True):
        last_promo_time = timezone.now() - datetime.timedelta(minutes=promo_config.promote_interval)
        promo_tasks = []
        if promo_config.last_run_time is None or promo_config.last_run_time < last_promo_time:
            promo_tasks.append(
                promote_instagram_by_following.s(promo_config.id)
            )
        celery.group(promo_tasks).apply_async()
