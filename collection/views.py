from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from collection.models import Collection, CollectionCard
from db.models import Card


@login_required
def collection_create(request):

    context = {
    }

    return render(request, 'collection/collection_create.html', context=context)

@login_required
def collection_detail(request, collection_slug, user_name):

    user_collection = Collection.objects.filter(
                    slug=collection_slug,
                    owner__username=user_name
                    ).get()

    context = {
        'collection': user_collection,
    }

    return render(request, 'collection/collection_detail.html', context=context)

@login_required
def add_card_to_collection(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    collectioncard, created = CollectionCard.objects.get_or_create(
                   collection_id=request.user.collection.id,
                   card_id=card.id
                   )

    collectioncard.count = F('count') + 1
    collectioncard.save()

    return redirect(reverse(
        'collection:collection_detail',
        kwargs={
            'collection_slug': request.user.collection.slug,
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
        collectioncard.count = F('count') - 1
        collectioncard.save()
    else:
        collectioncard.delete()

    return redirect(reverse(
        'collection:collection_detail',
        kwargs={
            'collection_slug': request.user.collection.slug,
            'user_name': request.user,
        }
    ))
