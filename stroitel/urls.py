"""stroitel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from core.auth.views import register, LoginView, LogoutView
from core.views import contacts
from news.views import NewsListView, GuideListView, InitiativesListView, DocsListView


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),

    path('admin/', admin.site.urls),

    path('', NewsListView.as_view(), name='news_list'),
    path('guide/', GuideListView.as_view(), name='guide_list'),
    path('docs/', DocsListView.as_view(), name='docs_list'),
    path('initiatives/', InitiativesListView.as_view(), name='initiatives_list'),

    path('site/', include('news.urls')),
    path('billing/', include('billing.urls')),

    path('contacts/', contacts, name='contacts'),

    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
