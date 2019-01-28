import operator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.views.decorators.http import require_POST

from functools import reduce
# from itertools import filter

from db.models import Card, Collection
from db.forms import CollectionAddCardForm

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

# @login_required
class CollectionDetailView(generic.DetailView):
    model = Collection

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            Collection,
            ### THIS CAUSES remove/card_slug to aooear
            # the same as collection_detail when uncommented
            #owner=self.request.user,
            name=self.kwargs['collection_name'],
            # id=self.kwargs['id']
            )

    # def get_context_data(self, **kwargs):
    #     context = super(CollectionDetailView, self).get_context_data(**kwargs)
    #     context['collection_name'] = self.object.name
    #     context['user_name'] = self.request.user.username
    #     return context


@login_required
@require_POST
def collection_add(request, card_id):
    pass
    # # collection = Collection(request)
    # card = get_object_or_404(Card, id=card_id)
    # form = CollectionAddCardForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     collection.add(card=card)
    # return redirect('collection_detail')

@login_required
def collection_remove(request, card_slug):
    card = get_object_or_404(Card, slug=card_slug)
    # collection, created = Collection.objects.get_or_create(owner=self.request.user.id)
    collection = Collection.objects.get(owner=1)
    collection.cards.remove(card)
    # card_qty = CollectionCards.objects.get(
    #     collection=self.request.context['collection'],
    #     card=card
    # )
    #
    # if card_qty.count > 0:
    #     card_qty.count -= 1
    #     card_qty.save()
    # else:
    #     card_qty.

    # return redirect(reverse(
    #     'collection_detail',
    #     kwargs={
    #         'collection_name': self.collection.name,
    #         'user_name': self.request.user.username,
    #     }
    # ))

    return render(request, 'card_list')
