from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms

from news.models import NewsEntry, SiteSection


class SiteSectionAdmin(admin.ModelAdmin):
    ordering = ('title',)


class SiteSectionInlineFormSet(forms.BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('site_section')


class SiteSectionInline(admin.TabularInline):
    formset = SiteSectionInlineFormSet
    model = SiteSection.news.through
    verbose_name = "Раздел сайта"
    verbose_name_plural = "Видна в разделах"
    fields = ('site_section', 'custom_short_text')


class NewsEntryForm(forms.ModelForm):
    short_text = forms.CharField(widget=CKEditorWidget(), label='Короткое описание')
    long_text = forms.CharField(widget=CKEditorWidget(), label='Полный текст (не обязательно)', required=False)

    class Meta:
        model = NewsEntry
        fields = ('published_at', 'title', 'short_text', 'long_text')


class NewsEntryAdmin(admin.ModelAdmin):
    form = NewsEntryForm
    ordering = ('-published_at',)

    inlines = [
        SiteSectionInline,
    ]


admin.site.register(NewsEntry, NewsEntryAdmin)
admin.site.register(SiteSection, SiteSectionAdmin)