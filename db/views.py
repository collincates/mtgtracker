from django.shortcuts import render
from django.views import generic
from db.models import Card

class CardListView(generic.ListView):
    model = Card
    paginate_by = 50

class CardDetailView(generic.DetailView):
    model = Card
    
