from django import forms

class CollectionAddCardForm(forms.Form):
    """Adds a card to the logged-in user's collection."""
    add = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
