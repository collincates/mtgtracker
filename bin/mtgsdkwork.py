# Alias these to avoid namespace conflicts
from mtgsdk import Card as SDKCard
from db.models import Card as Card


class CardGrabber(object):
    """
    Instantiate this class to retreive all card objects from
    MTGSDK and store the card objects in self.cards.

    When calling the method self._change_id_field_name:
    obj.__dict__['id']    becomes    obj.__dict__['sdk_id']
    to avoid ValueError in Django's AutoField when creating
    model objects from the card objects stored in self.cards.
    """
    def __init__(self):
        self.cards = []
        self._get_cards()
        self._change_id_field_name()
    def _get_cards(self):
        """
        Paginate through MTGSDK and retrieve all Card objects.

        Upper range limit of 500 will need to be changed as
        more sets/cards are added to the game.
        """
        for i in range(1, 500):
            self.cards.extend(Card.where(page=i).all())
            print(f'got page {i}')
    def _change_id_field_name(self):
        """
        MTGSDK provides a UUID for every card in the SDK.

        From the MTGSDK docs:

            'id' - A unique (string) id for this card.
            It is made up by doing an SHA1 hash
            of setCode + cardName + cardImageName.

            e.g. '58d469f5-998a-5dfa-93d4-355df6d38799'

        Leaving the key name as ['id'] raises a ValueError with Django's
        AutoField, which accepts integers and cannot accept string values.

        This method changes the key name from ['id'] to ['sdk_id'],
        allowing for a Card object's **kwargs to be passed into a
        Django Model's create() method without error, while retaining
        the intended functionality of Django's AutoField
        which acts as an auto-incrementing primary key.
        """
        for card in self.cards:
            card.__dict__['sdk_id'] = card.__dict__.pop('id')
            print(f'changed {self.cards.index(card)}')
        print(len(self.cards))


class CardModelFactory(object):
    def __init__(self, mtgsdk_card):
        if type(data) is str:
            data = json.loads(data)
        self.from_dict(data)
    def from_dict(self, data):
        for key, value in data.items():
            if value == 'true':
                value = 'True'
            if type(value) is dict:
                value = self.from_dict(value)
            self.__dict__[key] = value

    def create_model(self, model):


for card, attrs in data.items():
    # put these objects in a list of CardModelFactory(attrs)






class CardPrice(models.Model):
    card = models.ForeignKey(Card, related_name='prices')
    price_cfb = models.DecimalField(max_digits=12, decimal_places=4)
    price_csi = models.DecimalField(max_digits=12, decimal_places=4)
    price_scg = models.DecimalField(max_digits=12, decimal_places=4)
    price_tcg = models.DecimalField(max_digits=12, decimal_places=4)
    datetime = models.DateTimeField(auto_now_add=True)





classattrs = ['artist', 'border', 'cmc', 'color_identity', 'colors', 'flavor', 'foreign_names', 'hand', 'id', 'image_url', 'layout', 'legalities', 'life', 'loyalty', 'mana_cost', 'multiverse_id', 'name', 'names', 'number', 'original_text', 'original_type', 'power', 'printings', 'rarity', 'release_date', 'rulings', 'set', 'set_name', 'source', 'starter', 'subtypes', 'supertypes', 'text', 'timeshifted', 'toughness', 'type', 'types', 'variations', 'watermark']

# attr = [ 'artist', 'border', 'cmc', 'colorIdentity', 'colors', 'contains', 'flavor', 'foreignNames', 'gameFormat', 'hand', 'id', 'imageUrl', 'language', 'layout', 'legalities', 'legality', 'life', 'loyalty', 'manaCost', 'multiverseid', 'name', 'names', 'number', 'orderBy', 'originalText', 'originalType', 'page', 'pageSize', 'power', 'printings', 'random', 'rarity', 'releaseDate', 'reserved', 'rulings', 'set', 'setName', 'source', 'starter', 'subtypes', 'supertypes', 'text', 'timeshifted', 'toughness', 'type', 'types', 'variations', 'watermark', ]
#
#
