from django.db.models import Prefetch, Count, Q
from django.utils.timezone import now

from social.models import Voting, VotingVariant


def get_voting(entry, user):
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
    return Voting.objects.filter(start_at__lte=dt_now, end_at__gte=dt_now).prefetch_related(
        Prefetch(
            'variants',
            queryset=VotingVariant.objects.annotate(
                cnt=Count("votes"),
            ).order_by('-cnt')
        )
    ).order_by('order', '-end_at').all()
