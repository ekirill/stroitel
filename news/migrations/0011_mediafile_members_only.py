# Generated by Django 3.1.5 on 2021-02-03 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_mediafile'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='members_only',
            field=models.BooleanField(default=False, verbose_name='Показывать только членам СНТ'),
        ),
    ]