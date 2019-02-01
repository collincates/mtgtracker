from django.urls import path, re_path
from . import views


app_name = 'db'

urlpatterns = [
    path('cards/', views.CardListView.as_view(), name='card_list'),
    re_path(r'^card/(?P<card_slug>[-\w]+)$', views.CardDetailView.as_view(), name='card_detail'),
]

    # path('<set_name>/', views.SetListView.as_view(), name='set_list'),
