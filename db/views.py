import logging

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
)

import operator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic

from functools import reduce
# from itertools import filter

from db.models import Card, ExpansionSet

class CardListView(generic.ListView):
    model = Card
    paginate_by = 100
    template_name = 'db/card_list.html'
    ordering = ['name']

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


class ExpansionSetListView(generic.ListView):
    allow_empty = False
    model = ExpansionSet
    paginate_by = 100
    template_name = 'db/expansionset_list.html'
    ordering = ['name']

    def get_queryset(self):
        return ExpansionSet.objects.all()


class ExpansionSetDetailView(generic.DetailView):
    model = ExpansionSet

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            ExpansionSet,
            slug=self.kwargs['set_slug'],
            # set_name=self.kwargs['set_slug'],
            )
