import operator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.views.decorators.http import require_POST

from functools import reduce
# from itertools import filter

from db.models import Card, Collection, CollectionCards
from db.forms import CollectionCardAddForm

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

@login_required
def collection_view(request, **kwargs):
    user_collection = Collection.objects.get(owner=request.user)
    collectioncards = CollectionCards.objects.filter(collection__owner=user_collection.owner)

    form = CollectionCardAddForm(request.POST)
    # for card in collectioncards.all():
    #     card['qty_update_form'] = CollectionCardAddForm(initial={'count': card['count']})

    context = {
        'collection': user_collection,
        # 'collection_name': user_collection.name,
        # 'user_name': user_collection.owner.username,
        'collectioncards': collectioncards,
        'form': form,
    }

    return render(request, 'db/collection_detail.html', context=context)

"""
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

    if request.POST:
        card_slug = request.POST.get('card_slug')
        card = Card.objects.get(slug=card_slug)
        # Make add/remove into if/then test
        if card not in collection.cards:
            CollectionCards.objects.create(
                collection=collection,
                card=card,
                count=1
            )
        else:
            collection.cards.add()
    # def get_context_data(self, **kwargs):
    #     context = super(CollectionDetailView, self).get_context_data(**kwargs)
    #     context['collection_name'] = self.object.name
    #     context['user_name'] = self.request.user.username
    #     return context
"""

@login_required
# @require_POST
def add_to_collection(request, collcard_id):
    collection = Collection.objects.get(owner=request.user)
    card = get_object_or_404(Card, id=collcard_id)
    # logic to add more quantities
    if request.method == 'POST':
        inst = CollectionCards.objects.get(collection_id=collection.id, card_id=card.id)
        form = CollectionCardAddForm(request.POST, instance=inst)
        if form.is_valid():
            collcard = form.save(commit=False)
            collcard.count = 10
            collcard.save()
            return redirect(reverse('collection_detail'))

    else:
        form = CollectionCardAddForm()

    messages.info(request, 'Card added to collection')
    return redirect(reverse('collection_detail'))

@login_required
def remove_from_collection(request, card_slug):
    collection = Collection.objects.get(owner=self.request.user)
    card = get_object_or_404(Card, slug=card_slug)
    collection.cards.remove(card)
    messages.info(request, 'Card has been removed from collection')
    return redirect(reverse('collection_detail'))

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
