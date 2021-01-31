from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms
from django.db.models import Q, Prefetch

from news.models import NewsEntry, SiteSection


class SiteSectionAdmin(admin.ModelAdmin):
    ordering = ('title',)


class SiteSectionInlineFormSet(forms.BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('site_section')


class SiteSectionInlineForm(forms.ModelForm):
    site_section = forms.ModelChoiceField(
        queryset=SiteSection.objects.filter(Q(parent__isnull=False) | Q(slug='news')),
        label='Раздел сайта',
    )

    class Meta:
        model = SiteSection.news.through
        fields = ('site_section',)


class SiteSectionInline(admin.TabularInline):
    formset = SiteSectionInlineFormSet
    form = SiteSectionInlineForm
    model = SiteSection.news.through
    verbose_name = "Раздел сайта"
    verbose_name_plural = "Видна в разделах"
    extra = 1


class NewsEntryForm(forms.ModelForm):
    short_text = forms.CharField(widget=CKEditorWidget(), label='Короткое описание')
    long_text = forms.CharField(widget=CKEditorWidget(), label='Полный текст (не обязательно)', required=False)

    class Meta:
        model = NewsEntry
        fields = ('published_at', 'title', 'short_text', 'long_text')


class NewsEntryAdmin(admin.ModelAdmin):
    form = NewsEntryForm
    ordering = ('-published_at',)
    list_display = ('title', 'published_at', 'get_site_section')

    inlines = [
        SiteSectionInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = qs.prefetch_related(
            Prefetch(
                'site_sections',
                queryset=SiteSection.objects.order_by('news_binds__order', 'news_binds__pk'),
            )
        )

        return qs

    def get_site_section(self, obj):
        sections = list(obj.site_sections.all())
        if len(sections) == 1:
            return str(sections[0])

        for section in sections:
            if section.slug == 'news':
                continue

            return str(section)

    get_site_section.short_description = 'Раздел'


admin.site.register(NewsEntry, NewsEntryAdmin)
admin.site.register(SiteSection, SiteSectionAdmin)
