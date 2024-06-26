# Generated by Django 3.2.13 on 2022-05-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_auto_20220514_1120'),
        ('posters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('page_id', models.CharField(max_length=30)),
                ('access_token', models.CharField(max_length=250)),
                ('app_id', models.CharField(max_length=30)),
                ('app_secret', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('hashtags', models.CharField(max_length=50, null=True, blank=True)),
                ('reddit_sources', models.ManyToManyField(to='crawlers.RedditSource')),
            ],
        ),
    ]
