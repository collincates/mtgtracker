from django.conf import settings
from django.db import models
from django.urls import reverse

from db.models import Card, Deck


class Collection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collection'
    )
    decks = models.ManyToManyField(Deck, related_name='collections')
    cards = models.ManyToManyField(Card, through='CollectionCard', related_name='collections')

    class Meta:
        ordering = ('name',)
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection:collection_detail',
            kwargs={
                'collection_name': self.name,
                'user_name': self.owner.username
            }
        )


class CollectionCard(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='collectioncards'
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='collectioncards'
    )

    count = models.PositiveSmallIntegerField()
        #What about land cards?
    class Meta:
        unique_together = ('card', 'collection',)
