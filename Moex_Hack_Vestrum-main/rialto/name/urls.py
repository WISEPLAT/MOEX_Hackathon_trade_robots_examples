from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.dashboard, name='dashboard'),
    path('analytics', views.analytics, name='analytics'),
    path('newsline', views.newsline, name='newsline'),
    path('news', views.news, name='news'),
    path('account', views.account, name='account'),
    path('wallet', views.wallet, name='wallet'),
    path('catalogue', views.catalogue, name='catalogue'),
    path('review', views.review, name='review'),
    path('catalogue2', views.catalogue2, name='catalogue2')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)