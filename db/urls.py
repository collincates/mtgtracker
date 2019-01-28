from django.urls import path
from . import views


urlpatterns = [
    # path('', )
    # path('', views.BrowseDatabaseView, name='browse-database'),
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('<set_name>/', views.SetListView.as_view(), name='set_list'),
    path('card/<card_slug>', views.CardDetailView.as_view(), name='card_detail'),
    path('<user_name>/<collection_name>/', views.collection_view, name='collection_detail'),
    # path('<user_name>/<collection_name>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('add/<card_slug>/', views.add_to_collection, name='collection_add'),
    path('remove/<card_slug>/', views.remove_from_collection, name='collection_remove'),
]
