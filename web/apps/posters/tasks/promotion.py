import logging
import random
import time

from django.utils import timezone

from apps.posters.models import InstagramLikePromoteConfig, InstagramHashtagFollowPromoteConfig
from apps.posters.utils import init_client, is_valid_account_to_follow
from dj_imposter.celery import app

logger = logging.getLogger('celery')


@app.task
def promote_instagram_by_like(like_config_pk: int):
    like_promotion = InstagramLikePromoteConfig.objects.select_related('profile').get(pk=like_config_pk)
    client = init_client(like_promotion.profile)
    medias = client.hashtag_medias_recent(like_promotion.hashtag, amount=like_promotion.likes_per_promotion)
    for media in medias:
        try:
            client.media_like(media.id)
        except Exception as e:
            logger.error(
                f'Failed to promote insta {like_promotion.profile.name} details: {e}'
            )
        else:
            time.sleep(random.randint(3, 10))
    like_promotion.last_run_time = timezone.now()
    like_promotion.save(update_fields={'last_run_time'})


@app.task
def promote_instagram_by_following(follow_config_pk: int):
    follow_promotion = InstagramHashtagFollowPromoteConfig.objects.select_related('profile').get(pk=follow_config_pk)
    client = init_client(follow_promotion.profile)

    followed_cnt = 0
    expand_attempt = 0
    search_cnt = follow_promotion.follow_per_promotion * 3  # because not every account will be followed
    search_media_kwargs = {
        'max_amount': search_cnt,
        'tab_key': 'recent'
    }
    while followed_cnt < follow_promotion.follow_per_promotion and expand_attempt < 3:
        expand_attempt += 1
        medias, cursor = client.hashtag_medias_v1_chunk(
            follow_promotion.hashtag,
            **search_media_kwargs
        )
        search_media_kwargs['max_id'] = cursor
        for media in medias:
            try:
                user_info = client.user_info(media.user.pk)
                is_valid_account = is_valid_account_to_follow(user_info)
                if is_valid_account:
                    is_followed = client.user_follow(user_info.pk)
                    if is_followed:
                        followed_cnt += 1
            except Exception as e:
                logger.error(
                    f'Failed to promote insta {follow_promotion.profile.name} details: {e}'
                )
            else:
                if followed_cnt >= follow_promotion.follow_per_promotion:
                    break
                time.sleep(random.randint(5, 10))
    follow_promotion.last_run_time = timezone.now()
    follow_promotion.save(update_fields={'last_run_time'})
