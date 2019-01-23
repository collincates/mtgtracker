from django.urls import path
from . import views


urlpatterns = [
    # path('', )
    path('cards/', views.CardListView.as_view(), name='card_list'),
    path('<set_name>/', views.SetListView.as_view(), name='set_list'),
    path('card/<card_slug>', views.CardDetailView.as_view(), name='card_detail'),
]
