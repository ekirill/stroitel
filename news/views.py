from urllib.parse import quote_plus

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.db.models import Prefetch, Count, Case, When
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView

from news.models import NewsEntry, SiteSection
from news.services.media import is_members_only
from social.models import Comment, VotingVariant, Vote
from social.services.comments import annotate_news_with_comments_info, get_grouped_comments
from social.services.voting import get_voting, get_active_votings


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

    @cached_property
    def extra_context(self):
        ctx = {
            'comments': get_grouped_comments(self.get_object()),
            'voting': get_voting(self.get_object(), self.request.user),
        }
        if self.site_section:
            ctx['page'] = self.site_section.slug
            if self.site_section.parent:
                ctx.update({
                    'page': self.site_section.parent.slug,
                    'sub_page': self.site_section.slug,
                })

        return ctx

    def _save_comment(self, request):
        obj = self.get_object()
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

    @transaction.atomic
    def _save_vote(self, request):
        obj = self.get_object()
        voting = obj.votings.first()
        if not voting or not voting.is_active:
            return

        variant_ids = set()

        new_variant = request.POST.get("voting_variant_new_text")
        if new_variant:
            variant, _ = VotingVariant.objects.get_or_create(
                voting=voting, variant=new_variant, defaults={"author": request.user}
            )
            variant_ids.add(variant.pk)

        for arg, val in request.POST.items():
            if arg.startswith("vote_for_"):
                try:
                    variant_id = int(arg.split("_")[-1])
                    variant_ids.add(variant_id)
                except (TypeError, ValueError):
                    pass

        existing_votes = set(
            Vote.objects.filter(
                variant__voting=voting, user=request.user
            ).values_list("variant_id", flat=True)
        )

        del_variant_ids = existing_votes.difference(variant_ids)
        new_variant_ids = variant_ids.difference(existing_votes)

        new_votes = []
        for v_id in new_variant_ids:
            new_votes.append(Vote(user=request.user, variant_id=v_id))
        Vote.objects.bulk_create(new_votes)

        for variant_id in del_variant_ids:
            Vote.objects.filter(variant_id=variant_id, user=request.user).delete()

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.members_only and not request.user.is_authenticated:
            return redirect_to_login(request.build_absolute_uri(), settings.LOGIN_URL, 'next')

        anchor = ''
        submit = request.POST.get('submit')
        if submit == 'comment':
            self._save_comment(request)
            anchor = '#commentsLatest'
        elif submit == 'vote':
            self._save_vote(request)
            anchor = '#voting'

        redirect_url = resolve_url('news_detail', pk=obj.pk) + anchor
        return HttpResponseRedirect(redirect_url)


class SiteSectionView(ListView):
    template_name = 'news/list.html'
    paginate_by = 5

    def get_queryset(self):
        return NewsEntry.objects.\
            filter(site_sections=self.site_section).\
            annotate(votings_cnt=Count("votings", )). \
            order_by('order', '-published_at')

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

    def get_paginate_by(self, queryset):
        if self.root_section.slug == 'votings':
            return 100

        return self.paginate_by

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
    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='news')

    @property
    def extra_context(self):
        ctx = super().extra_context
        ctx['active_votings'] = get_active_votings()

        return ctx


class GuideListView(SiteSectionView):
    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='guide')


class DocsListView(SiteSectionView):
    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='documents')


class InitiativesListView(SiteSectionView):
    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='initiatives')


class VotingsListView(SiteSectionView):
    @cached_property
    def site_section(self):
        return get_object_or_404(SiteSection, slug='votings')


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
