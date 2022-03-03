# Generated by Django 3.1.5 on 2022-02-19 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0016_sitesection_order'),
        ('social', '0003_auto_20210308_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2000, verbose_name='Вопрос')),
                ('entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.newsentry', verbose_name='Документ')),
            ],
            options={
                'verbose_name': 'Голосование',
                'verbose_name_plural': 'Голосования',
            },
        ),
        migrations.CreateModel(
            name='VotingVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('variant', models.TextField(verbose_name='Вариант')),
                ('order', models.IntegerField(default=100, verbose_name='Порядок')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='social.voting', verbose_name='Голосование')),
            ],
            options={
                'verbose_name': 'Вариант ответов',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
    ]