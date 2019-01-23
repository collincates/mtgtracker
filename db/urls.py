from django.urls import path
from . import views


urlpatterns = [
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('cards/<set_name>/', views.SetListView.as_view(), name='set_list'),
    path('<card_slug>', views.CardDetailView.as_view(), name='card_detail'),
]
