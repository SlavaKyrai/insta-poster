import logging

from django.utils import timezone

from apps.crawlers.models import Post
from apps.posters.models import InstagrapiConfig
from apps.posters.utils import init_client, temp_file_from_url, get_instagram_post_data

logger = logging.getLogger('celery')


class InstagramService:

    def __init__(self, instagram_config: InstagrapiConfig):
        self.config = instagram_config
        self.client = init_client(instagram_config)

    def post_photo(self, post: Post) -> bool:
        try:
            with temp_file_from_url(post.image_url) as file_name:
                data = get_instagram_post_data(
                    file_name,
                    post,
                    self.config,
                    self.client
                )
                self.client.photo_upload(
                    path=data.path,
                    caption=data.caption,
                    location=data.location
                )
        except Exception as e:
            logger.error(
                f'Failed to post to insta {self.config.name} details: {e}'
            )
            return False
        else:
            self.config.last_post_date = timezone.now()
            self.config.save(update_fields={'last_post_date'})
            return True
        finally:
            post.is_instagram_posted = True
            post.save(update_fields={'is_instagram_posted'})
