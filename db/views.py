from django.shortcuts import get_object_or_404, render
from django.views import generic
from db.models import Card
from django.utils.text import slugify


class CardListView(generic.ListView):
    model = Card
    paginate_by = 5000

    def get_queryset(self):
        return Card.objects.filter(set='FEM')

class SetListView(generic.ListView):
    model = Card
    slug_field = 'set_name'
    slug_url_kwarg = 'set_name'

    def get_queryset(self, set_name):
        return Card.objects.filter(set_name=set_name)


class CardDetailView(generic.DetailView):
    model = Card
    # pk_field = 'id'
    # pk_url_kwarg = 'id'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
