from django.urls import path, re_path
from . import views


urlpatterns = [
    # path('', )
    # path('', views.BrowseDatabaseView, name='browse-database'),
    re_path(r'^(?P<user_name>[-\w]+)/(?P<collection_name>[-\w]+)/$', views.test_view, name='test_view'),
    path('adds/<card_id>/', views.test_add, name='test_add'),

    # path('cards/', views.CardListView.as_view(), name='card_list'),
    # path('<set_name>/', views.SetListView.as_view(), name='set_list'),
    path('card/<card_slug>', views.CardDetailView.as_view(), name='card_detail'),
    # path('<user_name>/<collection_name>/', views.collection_view, name='collection_detail'),
    # path('<user_name>/<collection_name>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    # path('add/<card_id>/', views.add_to_collection, name='collection_add'),
    # path('remove/<card_id>/', views.remove_from_collection, name='collection_remove'),
]
