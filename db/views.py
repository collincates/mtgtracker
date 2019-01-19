from django.shortcuts import get_object_or_404, render
from django.views import generic
from db.models import Card

class CardListView(generic.ListView):
    model = Card
    paginate_by = 5000

    def get_queryset(self):
        return Card.objects.filter(set='FEM')

class CardDetailView(generic.DetailView):
    model = Card
    pk_field = 'id'
    # pk_url_kwarg = 'id'
