from django.urls import path

from news.views import NewsEntryView, SiteSectionView, media_access


urlpatterns = [
    path('media/<prefix>/<path>', media_access, name='media'),
    path('entry/<int:pk>/', NewsEntryView.as_view(), name='news_detail'),
    path('<slug:slug>/', SiteSectionView.as_view(), name='site_section'),
]
