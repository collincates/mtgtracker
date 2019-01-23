from django.shortcuts import get_object_or_404, render
from django.views import generic
from db.models import Card
from django.utils.text import slugify


class CardListView(generic.ListView):
    model = Card
    paginate_by = 100

    # def get_queryset(self):
    #     return Card.objects.filter(set='LEA')

class SetListView(generic.ListView):
    model = Card
    paginate_by = 100

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
