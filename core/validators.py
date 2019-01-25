from django.core.exceptions import ValidationError

def validate_card_count(card):
    """Raise a ValidationError if a deck contains more than the legal number
    of copies of a card.

    This number is (4) for all cards except for:

    Basic Lands
    Snow-covered Lands
    Relentless Rats.

    """

    if not card.supertypes in ('Snow', 'Basic',) or card.name == 'Relentless Rats':
        #card count == 4
        pass
