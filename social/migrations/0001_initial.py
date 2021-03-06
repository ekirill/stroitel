# Generated by Django 3.1.5 on 2021-02-11 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0016_sitesection_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Виден всем')),
                ('message', models.CharField(max_length=2000, verbose_name='Сообщение')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.newsentry', verbose_name='Документ')),
                ('reply_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='social.comment', verbose_name='Ответ на')),
            ],
        ),
    ]