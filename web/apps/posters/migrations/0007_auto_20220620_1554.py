# Generated by Django 3.2.13 on 2022-06-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posters', '0006_auto_20220615_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagrapiconfig',
            name='mention_author',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instagrapiconfig',
            name='use_location_in_post',
            field=models.BooleanField(default=True),
        ),
    ]
