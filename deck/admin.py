from django.contrib import admin

from deck.models import Deck
from db.models import Card

class CardsInline(admin.TabularInline):
    model = Deck.cards.through
    extra = 1

@admin.register(Deck)
class DeckModelAdmin(admin.ModelAdmin):
    inlines = [CardsInline]
    exclude = ('cards',)

    list_display = ('name', 'description', 'owner')

    def get_queryset(self, request):
        qs = super(DeckModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(collection__owner=request.user)

    # def get_readonly_fields(self, request, obj=None):
    #     return [f.name for f in self.model._meta.fields]

    def owner(self, deck):
        return deck.collections.filter(
            owner__username='ccc').first().owner.username
    #
    # def deck_cards(self, obj):
    #     return "\n".join([card.name for card in obj.cards.all()])
