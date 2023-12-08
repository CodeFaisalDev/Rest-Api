# Generated by Django 4.2.5 on 2023-10-09 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0010_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='average_review',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]
