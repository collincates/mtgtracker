from django.contrib import admin

from collection.models import Collection


@admin.register(Collection)
class CollectionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
