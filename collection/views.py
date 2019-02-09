from django.contrib.auth.decorators import login_required
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
def collection_view(request, collection_slug, user_name):

    user_collection = Collection.objects.filter(
                    slug=collection_slug,
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
        collectioncard.count -= 1
        collectioncard.save()
    else:
        collectioncard.delete()

    return redirect(reverse(
        'collection:collection_view',
        kwargs={
            'collection_slug': request.user.collection.slug,
            'user_name': request.user,
        }
    ))
