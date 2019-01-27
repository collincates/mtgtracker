from django.urls import path
from . import views


urlpatterns = [
    # path('', )
    # path('', views.BrowseDatabaseView, name='browse-database'),
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('<set_name>/', views.SetListView.as_view(), name='set_list'),
    path('card/<card_slug>', views.CardDetailView.as_view(), name='card_detail'),
    path('<user_name>/<collection_name>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('add/<card_id>/', views.collection_add, name='collection_add'),
    path('remove/<card_id>/', views.collection_remove, name='collection_remove'),
]
