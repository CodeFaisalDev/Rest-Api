# Generated by Django 4.2.5 on 2023-10-02 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_watchlist_stream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='stream',
        ),
    ]