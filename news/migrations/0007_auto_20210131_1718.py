# Generated by Django 3.1.5 on 2021-01-31 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20210131_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesection',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL slug'),
        ),
    ]
