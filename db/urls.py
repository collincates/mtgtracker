from django.urls import path, re_path
from . import views


urlpatterns = [
    path('cards/', views.CardListView.as_view(), name='card_list'),
    re_path(r'^add/(?P<card_id>\d+)/$', views.add_card_to_collection, name='collection_add'),
    re_path(r'^remove/(?P<card_id>\d+)/$', views.remove_card_from_collection, name='collection_remove'),
    re_path(r'^collection/(?P<user_name>[-\w]+)/(?P<collection_name>[-\w]+)/$', views.collection_view, name='collection_view'),
    re_path(r'^card/(?P<card_slug>[-\w]+)$', views.CardDetailView.as_view(), name='card_detail'),
]

    # path('<set_name>/', views.SetListView.as_view(), name='set_list'),
    # path('<user_name>/<collection_name>/', views.collection_view, name='collection_detail'),
    # path('<user_name>/<collection_name>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    # path('add/<card_id>/', views.add_to_collection, name='collection_add'),
    # path('remove/<card_id>/', views.remove_from_collection, name='collection_remove'),
