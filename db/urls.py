from django.urls import path, re_path
from . import views


app_name = 'db'

urlpatterns = [
    re_path(r'^cards/$', views.CardListView.as_view(), name='card_list'),
    re_path(r'^card/(?P<card_slug>[-\w]+)$', views.CardDetailView.as_view(), name='card_detail'),
    re_path(r'^expansions/$', views.ExpansionSetListView.as_view(), name='set_list'),
    re_path(r'^expansion/(?P<set_slug>[-\w]+)$', views.ExpansionSetDetailView.as_view(), name='set_detail'),
]
