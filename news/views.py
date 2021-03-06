from urllib.parse import quote_plus

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView

from news.models import NewsEntry, SiteSection
from news.services.media import is_members_only
from social.models import Comment
from social.services.comments import annotate_news_with_comments_info, get_grouped_comments


class NewsEntryView(DetailView):
    _object = None

    queryset = NewsEntry.objects.prefetch_related(
        Prefetch(
            'section_binds',
            queryset=NewsEntry.site_sections.through.objects.select_related('site_section').order_by('order', 'pk'),
        ),
    )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.members_only and not request.user.is_authenticated:
            return redirect_to_login(request.build_absolute_uri(), settings.LOGIN_URL, 'next')

        return super().get(request, *args, **kwargs)

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
        ctx = {
            'comments': get_grouped_comments(self.get_object()),
        }
        if self.site_section:
            ctx['page'] = self.site_section.slug
            if self.site_section.parent:
                ctx.update({
                    'page': self.site_section.parent.slug,
                    'sub_page': self.site_section.slug,
                })

        return ctx

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.members_only and not request.user.is_authenticated:
            return redirect_to_login(request.build_absolute_uri(), settings.LOGIN_URL, 'next')

        message = (request.POST.get('message') or '').strip()
        if message:
            # защита от двойного нажатия
            user_latest_comment = Comment.objects.filter(
                author=request.user, entry=obj
            ).order_by('-published_at').first()
            if not user_latest_comment or user_latest_comment.message != message:
                Comment.objects.create(
                    entry=obj,
                    author=request.user,
                    message=message[:settings.MAX_COMMENT_SIZE],
                )

        redirect_url = resolve_url('news_detail', pk=obj.pk) + '#commentsLatest'
        return HttpResponseRedirect(redirect_url)


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
        return list(SiteSection.objects.filter(parent=self.root_section).order_by('order', 'title').all())

    @property
    def extra_context(self):
        ctx = {
            'page': self.root_section.slug,
            'section': self.site_section,
            'child_sections': self.child_sections,
        }

        return ctx

    def paginate_queryset(self, queryset, page_size):
        paginator, page, object_list, has_other_pages = super().paginate_queryset(queryset, page_size)
        object_list = list(object_list)
        annotate_news_with_comments_info(object_list)
        return paginator, page, object_list, has_other_pages

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


class DocsListView(SiteSectionView):
    queryset = NewsEntry.objects.order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='documents')


class InitiativesListView(SiteSectionView):
    queryset = NewsEntry.objects.order_by('-published_at')

    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='initiatives')


def media_access(request, prefix, path):
    full_name = f"{prefix}/{path}"
    if is_members_only(full_name):
        if not request.user.is_authenticated:
            return redirect_to_login(request.build_absolute_uri(), settings.LOGIN_URL, 'next')

    response = HttpResponse()
    # Content-type will be detected by nginx
    del response['Content-Type']
    response['X-Accel-Redirect'] = '/protected_media/' + quote_plus(full_name)
    return response
