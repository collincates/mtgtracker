import operator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views import generic
from db.models import Card, Collection
from django.utils.text import slugify
from functools import reduce
# from itertools import filter

class CardListView(generic.ListView):
    model = Card
    paginate_by = 100
    template_name = 'db/card_list.html'


    def get_queryset(self):
        result=super(CardListView, self).get_queryset()

        query = self.request.GET.get('query')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                    (Q(name__icontains=q) for q in query_list))
            )

        return result

class SetListView(generic.ListView):
    allow_empty = False
    model = Card
    paginate_by = 100
    template_name = 'db/set_list.html'

    def get_queryset(self):
        return Card.objects.filter(set_name=self.kwargs['set_name'])


class CardDetailView(generic.DetailView):
    model = Card

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            Card,
            slug=self.kwargs['card_slug'],
            # set_name=self.kwargs['set_slug'],
            )

class CollectionDetailView(generic.DetailView):
    model = Collection

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            Collection,
            # user_name=self.kwargs['user_name'],
            name=self.kwargs['collection_name'],
            # id=self.kwargs['id']
            )

    # def get_queryset(self):
    #     return Collection.objects.get(owner=self.kwargs['user_name'])
