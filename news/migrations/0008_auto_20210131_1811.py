# Generated by Django 3.1.5 on 2021-01-31 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20210131_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsentry',
            name='long_text',
            field=models.TextField(blank=True, null=True, verbose_name='Полный текст'),
        ),
    ]