import logging

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
)

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from collection.models import Collection, CollectionCard
from db.models import Card


@login_required
def collection_create(request):
    pass

@login_required
def collection_view(request, collection_name, user_name):

    user_collection = Collection.objects.filter(
                    name=collection_name,
                    owner__username=user_name
                    ).get()

    context = {
        'collection': user_collection,
    }

    return render(request, 'collection/collection_view.html', context=context)

@login_required
def add_card_to_collection(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    try:
        collectioncard = CollectionCard.objects.get(
                       collection_id=request.user.collection.id,
                       card_id=card.id
                       )

        collectioncard.count += 1
        collectioncard.save()

    except CollectionCard.DoesNotExist:
        collectioncard = CollectionCard.objects.create(
                       collection_id=request.user.collection.id,
                       card_id=card.id,
                       count=1
                       )

    return redirect(reverse(
        'collection:collection_view',
        kwargs={
            'collection_name': request.user.collection.name,
            'user_name': request.user,
        }
    ))

@login_required
def remove_card_from_collection(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    collectioncard = CollectionCard.objects.get(
                   collection_id=request.user.collection.id,
                   card_id=card.id
                   )

    if collectioncard.count > 1:
        collectioncard.count -= 1
        collectioncard.save()
    else:
        collectioncard.delete()

    return redirect(reverse(
        'collection:collection_view',
        kwargs={
            'collection_name': request.user.collection.name,
            'user_name': request.user,
        }
    ))

#
# @login_required
# def collection_view(request, **kwargs):
#     user_collection = Collection.objects.get(owner=request.user, name=collection_name)
#     collectioncards = CollectionCard.objects.filter(collection__owner=user_collection.owner)
#
#
#     context = {
#         'collection': user_collection,
#         'collectioncards': collectioncards,
#     }
#
#     return render(request, 'db/collection_detail.html', context=context)

#
# @login_required
# def add_to_collection(request, card_id):
#     user_collection = Collection.objects.get(owner=request.user)
#     collectioncards = CollectionCard.objects.filter(collection__owner=user_collection.owner)
#     card = get_object_or_404(Card, id=card_id)
#     collcardcount = card.collectioncards.all().first().count
#     # logic to add more quantities
#     try:
#         collcard = CollectionCard.objects.get(collection_id=user_collection.id, card_id=card.id, count=collcardcount)
#     except CollectionCard.DoesNotExist:
#         collcard = CollectionCard.objects.get(collection_id=user_collection.id, card_id=card.id, count=1)
#
#     # if card_qty.count > 0:
#     #     card_qty.count -= 1
#     #     card_qty.save()
#     # else:
#     #     card_qty.
#
#
#     collcard.count = 10
#     collcard.save()
#
#     messages.info(request, 'Card added to collection')
#
#     return redirect(reverse(
#         'collection_detail',
#         kwargs={
#             'collection_name': user_collection.name,
#             'user_name': user_collection.owner.username,
#         }
#     ))


# @login_required
# def remove_from_collection(request, card_slug):
#     collection = Collection.objects.get(owner=request.user)
#     card = get_object_or_404(Card, slug=card_slug)
#     collection.cards.remove(card)
#     messages.info(request, 'Card has been removed from collection')
#     return redirect(reverse('collection_detail'))
