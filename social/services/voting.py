from collections import defaultdict

from django.db.models import Prefetch, Count, Q
from django.utils.timezone import now

from news.models import SiteSection, NewsEntryBind, NewsEntry
from social.models import Voting, VotingVariant


def get_voting(entry: NewsEntry, user):
    voting = Voting.objects.filter(entry=entry).first()
    if not voting:
        return None

    variants_for_user = VotingVariant.objects.filter(voting=voting).annotate(
        user_voted=Count("votes", filter=Q(votes__user=user))
    ).order_by('order', '-published_at').all()
    voting_results = VotingVariant.objects.filter(voting=voting).annotate(
        cnt=Count("votes"),
    ).order_by('-cnt', 'order', '-published_at').all()

    return {
        'voting': voting,
        'variants_for_user': variants_for_user,
        'voting_results': voting_results,
    }


def get_active_votings():
    dt_now = now()

    grouped_by_entries_votings = {}
    v_q = Voting.objects.filter(start_at__lte=dt_now, end_at__gte=dt_now).order_by('order', '-end_at').all()
    voting_order = {}
    for order, voting in enumerate(v_q):
        grouped_by_entries_votings[voting.entry_id] = voting
        voting_order[voting.pk] = order

    grouped_votings = defaultdict(lambda: dict(section_title=0, votings=[]))
    q = NewsEntryBind.objects.filter(
        news_entry_id__in=grouped_by_entries_votings.keys(), site_section__parent__slug='votings'
    ).values_list("news_entry_id", "site_section__title", "site_section__slug")
    for news_entry_id, site_section_title, site_section_slug in q:
        grouped_votings[site_section_slug]["votings"].append(grouped_by_entries_votings[news_entry_id])
        grouped_votings[site_section_slug]["section_title"] = site_section_title

    for item in grouped_votings.values():
        item["votings"].sort(key=lambda v: voting_order[v.pk])

    grouped_votings = dict(grouped_votings)

    return grouped_votings
