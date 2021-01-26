from django.db import models


class NewsEntry(models.Model):
    published_at = models.DateTimeField('Дата публикации')
    title = models.CharField('Заголовок', max_length=1024)
    short_text = models.TextField('Короткое описание')
    long_text = models.TextField('Полный текст')

    def full_text(self):
        return self.long_text or self.short_text

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
