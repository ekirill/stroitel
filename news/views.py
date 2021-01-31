from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView

from news.models import NewsEntry, SiteSection


class NewsEntryView(DetailView):
    _object = None

    queryset = NewsEntry.objects.prefetch_related(
        Prefetch(
            'section_binds',
            queryset=NewsEntry.site_sections.through.objects.select_related('site_section').order_by('order', 'pk'),
        ),
    )

    def get_object(self, queryset=None):
        if self._object is None:
            self._object = super().get_object(queryset)

        return self._object

    @cached_property
    def site_section(self):
        binds = self.get_object().section_binds.all()
        if binds:
            return binds[0].site_section

    @property
    def extra_context(self):
        if self.site_section:
            if self.site_section.parent:
                return {
                    'page': self.site_section.parent.slug,
                    'sub_page': self.site_section.slug,
                }

            return {'page': self.site_section.slug}


class SiteSectionView(ListView):
    template_name = 'news/list.html'
    paginate_by = 5

    def get_queryset(self):
        return NewsEntry.objects.\
            filter(site_sections=self.site_section).order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug=self.kwargs['slug'])

    @cached_property
    def root_section(self):
        return self.site_section and self.site_section.parent or self.site_section

    @cached_property
    def child_sections(self):
        return list(SiteSection.objects.filter(parent=self.root_section).order_by('title').all())

    @property
    def extra_context(self):
        ctx = {
            'page': self.root_section.slug,
            'section': self.site_section,
            'child_sections': list(SiteSection.objects.filter(parent=self.root_section).order_by('title').all()),
        }

        return ctx

    def get(self, request, *args, **kwargs):
        if not self.site_section.parent and len(self.child_sections):
            return redirect('site_section', slug=self.child_sections[0].slug)

        return super().get(request, *args, **kwargs)


class NewsListView(SiteSectionView):
    queryset = NewsEntry.objects.order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='news')


class GuideListView(SiteSectionView):
    queryset = NewsEntry.objects.order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='guide')


class InitiativesListView(SiteSectionView):
    queryset = NewsEntry.objects.order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='initiatives')
