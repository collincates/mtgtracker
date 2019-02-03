from django.contrib import admin

from deck.models import Deck
from db.models import Card

class DeckInline(admin.TabularInline):
    model = Deck.cards.through


@admin.register(Deck)
class DeckModelAdmin(admin.ModelAdmin):
    inlines = [DeckInline]

    list_display = ('name', 'description')

    # def get_readonly_fields(self, request, obj=None):
    #     return [f.name for f in self.model._meta.fields]

    def show_cards(self, obj):
        return '\n'.join([card.name for card in obj.cards.all()])

    def deck_cards(self, obj):
        return "\n".join([card.name for card in obj.cards.all()])
