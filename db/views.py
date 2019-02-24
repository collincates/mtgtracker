from collections import Counter
from functools import reduce
import logging

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
)

import operator
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic

from db.models import Card, ExpansionSet


def card_list(request):
    all_cards = Card.objects.all()
    query = request.GET.get('query')
    if query:
        query_list = query.split()
        all_cards = all_cards.filter(
            reduce(operator.and_,
                (Q(name__icontains=q) for q in query_list))
        )
    # Returns only latest printings of each card
    # This takes a long time to load!
    all_cards = all_cards.order_by('name', '-release_date').distinct('name')

    if all_cards.count() == 1:
        return redirect(reverse(
            'db:card_detail',
            kwargs={
                'card_slug': all_cards.first().slug
            }
        ))

    paginator = Paginator(all_cards, 100)
    page = request.GET.get('page')
    if not page:
        page = 1
    all_cards = paginator.get_page(page)

    if all_cards.paginator.num_pages > 7:
        if int(page) < 5:
            visible_page_links = [i for i in range(1, 8)]
        elif int(page) > all_cards.paginator.num_pages - 3:
            visible_page_links = [i for i in range((all_cards.paginator.num_pages - 6), all_cards.paginator.num_pages + 1)]
        else:
            visible_page_links = [i for i in range((int(page) - 3), (int(page) + 4))]
    elif all_cards.paginator.num_pages > 1:
        visible_page_links = [i for i in range(1, all_cards.paginator.num_pages + 1)]
    else:
        visible_page_links = None

    context = {
        'all_cards': all_cards,
        'visible_page_links': visible_page_links
    }

    return render(request, 'db/card_list.html', context)


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
    ordering = ['id']


class ExpansionSetDetailView(generic.DetailView):
    model = ExpansionSet

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            ExpansionSet,
            slug=self.kwargs['set_slug'],
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['set_cards'] = Card.objects.filter(set=self.object.code)
        # context['cards_by_color'] = self.get_card_count_by_color()
        return context


def expansionset_chart_data(self, set_slug):
    """
    Return a dictionary of card count by card color for a set.
    Colors are stored as dictionary keys and their counts
    are stored as dictionary values.
    """
    cards_by_color = Counter()
    set_cards = Card.objects.filter(
        expansionsetcards__expansionset_id__slug=set_slug
    )
    for card in set_cards:
        # Card is colorless
        if len(card.color_identity) == 0:
            # Card is a land
            # Card is an artifact
            # Card is a ??
            cards_by_color['colorless'] += 1
        elif len(card.color_identity) == 1:
            # Card is a single color
            cards_by_color[card.color_identity[0]] += 1
        elif len(card.color_identity) > 1:
            # Card is multicolor
            cards_by_color['multicolor'] += 1
        else:
            # Is there an else?
            pass
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Card Count by Color Identity'},
        'series': [{
            'name': 'Color Identities',
            'data': [{'name': k, 'y': v} for k, v in cards_by_color.items()]
        }]
    }

    # chart = {
    #     'chart': {'type': 'column'},
    #     'title': {'text': 'Card Count by Color Identity'},
    #     'series': [{
    #         'name': 'Color Identities',
    #         'data': [{
    #             'name': 'colorless',
    #             'color': '#967d48',
    #             'y': 65
    #         }, {
    #             'name': 'W',
    #             'color': '#fffbd5',
    #             'y': 7
    #         }, {
    #             'name': 'U',
    #             'color': '#aae0fa',
    #             'y': 7
    #         }, {
    #             'name': 'B',
    #             'color': '#cbc2bf',
    #             'y': 7
    #         }, {
    #             'name': 'R',
    #             'color': '#f9aa8f',
    #             'y': 7
    #         }, {
    #             'name': 'G',
    #             'color': '#9bd3ae',
    #             'y': 7
    #         }]
    #     }]
    # }
    return JsonResponse(chart)
