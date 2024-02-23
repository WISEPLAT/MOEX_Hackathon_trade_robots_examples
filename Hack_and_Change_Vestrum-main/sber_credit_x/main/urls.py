from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('workspace', views.workspace, name='workspace'),
    path('workspace1', views.workspace1, name='space_for_worker1'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)