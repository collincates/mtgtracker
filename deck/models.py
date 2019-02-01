from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from db.models import Card


class Deck(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.SlugField(max_length=150, null=False, unique=False)
    cards = models.ManyToManyField(
        Card,
        through='DeckCard',
        related_name='decks'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'deck'
        verbose_name_plural = 'decks'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}')
        super(Deck, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('deck:deck_detail', kwargs={'deck_slug': self.slug})


class DeckCard(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='deckcards'
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='deckcards'
    )

    count = models.PositiveSmallIntegerField()
        #What about land cards?
    class Meta:
        unique_together = ('card', 'deck',)

    def __str__(self):
        return self.name
