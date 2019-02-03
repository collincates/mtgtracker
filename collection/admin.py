from django.contrib import admin

from collection.models import Collection

class DecksInline(admin.TabularInline):
    model = Collection.decks.through

@admin.register(Collection)
class CollectionModelAdmin(admin.ModelAdmin):
    inlines = [DecksInline]
    exclude = ('decks',)

    list_display = ('name', 'owner',)
