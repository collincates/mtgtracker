from django import forms
from db.models import CollectionCards

QTY_CHOICES = [i for i in range(1, 4)]

# class CollectionAddCardForm(forms.Form):
#     """Adds a card to the logged-in user's collection."""
#
#     quantity = forms.TypedChoiceField(choices=QTY_CHOICES, coerce=int)
#     update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CollectionCardAddForm(forms.ModelForm):

    class Meta:
        model = CollectionCard
        fields = ('collection', 'card', 'count',)
