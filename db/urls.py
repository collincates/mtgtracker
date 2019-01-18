from django.urls import path
from . import views


urlpatterns = [
    path('cards/', views.CardListView.as_view(), name='cards'),
    path('card/<int:pk>/', views.CardDetailView.as_view(), name='card_detail'),
]
