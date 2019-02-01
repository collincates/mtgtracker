from django.urls import path, re_path
from . import views


app_name = 'deck'

urlpatterns = [
    re_path(r'^deck/(?P<deck_slug>[-\w]+)$', views.DeckDetailView.as_view(), name='deck_detail'),
]
