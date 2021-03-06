from django.db import models
from django.utils.timezone import now


class Comment(models.Model):
    entry = models.ForeignKey('news.NewsEntry', verbose_name='Документ', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey('core.StroiUser', verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    published_at = models.DateTimeField('Дата публикации', default=now, db_index=True)
    is_visible = models.BooleanField('Виден всем', default=True)
    reply_to = models.ForeignKey('social.Comment', verbose_name='Ответ на', null=True, on_delete=models.SET_NULL)
    message = models.CharField('Сообщение', max_length=2000)
