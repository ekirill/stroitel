from django.db.models import Count

from social.models import Comment


def annotate_news_with_comments_info(entries):
    comment_cnt = {
        item['entry_id']: item['cnt'] for item in
        Comment.objects.filter(entry__in=entries).values('entry_id').annotate(cnt=Count('entry_id'))
    }
    for entry in entries:
        entry.comment_count = comment_cnt.get(entry.pk, 0)


def get_grouped_comments(entry):
    return Comment.objects.filter(entry=entry).select_related('author').order_by('published_at')
