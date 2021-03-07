from django.db import models
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from django.utils.timezone import now


class Comment(models.Model):
    entry = models.ForeignKey('news.NewsEntry', verbose_name='Документ', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey('core.StroiUser', verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    published_at = models.DateTimeField('Дата публикации', default=now, db_index=True)
    is_visible = models.BooleanField('Виден всем', default=True)
    reply_to = models.ForeignKey('social.Comment', verbose_name='Ответ на', null=True, on_delete=models.SET_NULL)
    message = models.CharField('Сообщение', max_length=2000)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    @property
    def message_html(self):
        return mark_safe("<br />".join(map(escape, self.message.split("\n"))))

    @property
    def author_name(self):
        username = self.author.username
        if username == 'tanya':
            username = '76'
        if username == 'ekirill':
            username = '44'
        return f"Участок {username}"
