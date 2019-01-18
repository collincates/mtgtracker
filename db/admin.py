from django.contrib import admin
from .models import Card

class CardInline(admin.TabularInline):
    model = Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # list_per_page = 4000
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    show_full_result_count = False
    search_fields = ('name', 'artist', 'type')
    list_display = ('name', 'type', 'set_name', 'rarity', 'artist')
    list_filter = ('set_name', 'rarity',)


    # fieldsets = (
    #     ('Card Text', {
    #         'fields': ('text', 'rulings', 'printings')
    #     }),
    # )

    # Using multiverse_id gives us chronological sort!
    ordering = ['name', 'multiverse_id']
