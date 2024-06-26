# Generated by Django 3.2.13 on 2022-06-15 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_auto_20220514_1120'),
        ('posters', '0005_instagrapiconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagrapiconfig',
            name='last_post_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instagrapiconfig',
            name='posting_hashtags',
            field=models.TextField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instagrapiconfig',
            name='reddit_sources',
            field=models.ManyToManyField(to='crawlers.RedditSource', blank=True),
        ),
    ]
