from django.contrib import admin
from django.forms import BaseInlineFormSet

from news.models import NewsEntry, SiteSection


class SiteSectionAdmin(admin.ModelAdmin):
    ordering = ('title',)


class SiteSectionInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('site_section')


class SiteSectionInline(admin.TabularInline):
    formset = SiteSectionInlineFormSet
    model = SiteSection.news.through
    verbose_name = "Раздел сайта"
    verbose_name_plural = "Видна в разделах"
    fields = ('site_section', 'custom_short_text')


class NewsEntryAdmin(admin.ModelAdmin):
    ordering = ('-published_at',)

    inlines = [
        SiteSectionInline,
    ]


admin.site.register(NewsEntry, NewsEntryAdmin)
admin.site.register(SiteSection, SiteSectionAdmin)