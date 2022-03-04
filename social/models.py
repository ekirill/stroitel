from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from common.utils import author_name


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
        return author_name(self.author.username)


class Voting(models.Model):
    entry = models.ForeignKey(
        'news.NewsEntry', verbose_name='Документ', null=True, on_delete=models.SET_NULL, related_name='votings'
    )
    question = models.CharField("Вопрос", max_length=2000)
    order = models.IntegerField("Порядок", default=0)
    start_at = models.DateTimeField('Дата начала', default=now)
    end_at = models.DateTimeField('Дата окончания', default=now)

    def __str__(self):
        return self.question

    @property
    def is_active(self):
        return self.start_at <= now() <= self.end_at

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
        index_together = ["start_at", "end_at"]


class VotingVariant(models.Model):
    voting = models.ForeignKey(Voting, verbose_name="Опрос", on_delete=models.CASCADE, related_name="variants")
    author = models.ForeignKey('core.StroiUser', verbose_name='Автор', null=True, on_delete=models.SET_NULL)
    published_at = models.DateTimeField('Дата публикации', default=now, db_index=True)

    variant = models.TextField("Вариант")
    order = models.IntegerField("Порядок", default=100)

    def __str__(self):
        return f"{self.voting.question}: {self.variant}"

    @property
    def author_name(self):
        return author_name(self.author.username)

    class Meta:
        verbose_name = "Вариант ответов"
        verbose_name_plural = "Варианты ответов"
        ordering = ("order", "published_at")


class Vote(models.Model):
    user = models.ForeignKey('core.StroiUser', verbose_name='Голосовавший', null=True, on_delete=models.SET_NULL)
    variant = models.ForeignKey(VotingVariant, verbose_name='Ответ', on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField('Дата голосования', default=now)
