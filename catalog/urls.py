# coding: utf-8

from django.conf.urls import url, include
from .views import CategoryView,  CategoryDetailView

urlpatterns = [
    url(r'^$', CategoryView.as_view(), name = 'category'),
    url(r'^(?:(?P<id>\d+)/)?$', CategoryDetailView.as_view(), name = 'detail_category')
]
