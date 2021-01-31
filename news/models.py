from django.db import models


class SiteSection(models.Model):
    title = models.CharField('Описание', max_length=128, db_index=True)
    stroi_staff_only = models.BooleanField('Показывать только членам СНТ')
    slug = models.SlugField('URL slug', unique=True)
    parent = models.ForeignKey(
        'news.SiteSection',
        verbose_name='Родителький раздел',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} / {self.title}"
        else:
            return f"{self.title}"

    class Meta:
        verbose_name = 'Раздел сайта'
        verbose_name_plural = 'Разделы сайта'


class NewsEntry(models.Model):
    published_at = models.DateTimeField('Дата публикации')
    title = models.CharField('Заголовок', max_length=1024)
    short_text = models.TextField('Короткое описание')
    long_text = models.TextField('Полный текст', blank=True, null=True)
    site_sections = models.ManyToManyField(
        SiteSection,
        through='news.NewsEntryBind',
        verbose_name='Разделы сайта',
        related_name='news',
    )

    @property
    def full_text(self):
        return self.long_text or self.short_text

    @property
    def has_details(self):
        return self.long_text and self.long_text != self.short_text

    def __str__(self):
        return f"[{self.published_at:%Y-%m-%d}] {self.title}"

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class NewsEntryBind(models.Model):
    news_entry = models.ForeignKey(
        NewsEntry,
        verbose_name='Новость',
        on_delete=models.CASCADE,
        related_name='section_binds',
    )
    site_section = models.ForeignKey(
        SiteSection,
        verbose_name='Раздел сайта',
        on_delete=models.CASCADE,
        related_name='news_binds',
    )
    custom_short_text = models.TextField('Алтернативное описание (не обязательно)', null=True, blank=True)
    order = models.IntegerField('Порядок', default=0)

    def __str__(self):
        return f"Привязка к разделу {self.site_section.slug}"

    class Meta:
        verbose_name = 'Привязка к разделу'
        verbose_name_plural = 'Привязки к разделам'
