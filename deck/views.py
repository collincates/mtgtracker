from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views import generic

from deck.models import Deck


# @login_required
class DeckDetailView(generic.DetailView):
    model = Deck

    def get_object(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            Deck,
            slug=self.kwargs['deck_slug'],
            )

# decklistview?
