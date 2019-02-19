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
    ordering = ['name', '-release_date']

    def get_queryset(self):
        result = super(CardListView, self).get_queryset()

        query = self.request.GET.get('query')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                    (Q(name__icontains=q) for q in query_list))
            )
        # this takes a long time to load!
        only_latest_printings = result.order_by('name', '-release_date').distinct('name')

        return only_latest_printings


class CardDetailView(generic.DetailView):
    model = Card

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            Card,
            slug=self.kwargs['card_slug'],
            )

    def get_context_data(self, **kwargs):
        context = super(CardDetailView, self).get_context_data(**kwargs)
        context['set_slug'] = ExpansionSet.objects.get(code=self.object.set).slug
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['set_cards'] = Card.objects.filter(set=self.object.code)
        return context
