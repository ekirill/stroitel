from django.views.generic import ListView, DetailView

from news.models import NewsEntry


class NewsListView(ListView):
    paginate_by = 5
    queryset = NewsEntry.objects.order_by('-published_at')
    extra_context = {'page': 'news'}


class NewsEntryView(DetailView):
    model = NewsEntry
    extra_context = {'page': 'news'}
