from django.contrib import admin
from django.urls import path

from news.views import NewsEntryView


urlpatterns = [
    path('<int:pk>/', NewsEntryView.as_view(), name='news_detail'),
]
