import logging

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
)

from django.core.management.base import BaseCommand
# Alias these to avoid namespace conflicts
from mtgsdk import Card as SDKCard
from mtgsdk import Set
from db.models import Card as Card
from db.models import ExpansionSet, ExpansionSetCard


# def progress(count, total, status=''):
#     bar_len = 60
#     filled_len = int(round(bar_len * count / float(total)))
#     percents = round(100.0 * count / float(total), 1)
#     bar = '#' * filled_len + '-' * (bar_len - filled_len)
#     sys.stdout.write(f'bar, percents, "%", status')


class Command(BaseCommand):
    """
    Instantiate this class to retrieve all card objects from
    MTGSDK and store the card objects in self.cards.

    When calling the method self._change_id_field_name:
    obj.__dict__['id']    becomes    obj.__dict__['sdk_id']
    to avoid ValueError in Django's AutoField when creating
    model objects from the card objects stored in self.cards.
    """

    help = 'Populates database with cards from MTGSDK.'

    def __init__(self):
        super(Command, self).__init__()
        self.cards = []
        self.sets = []
        self.errors = []

    def handle(self, *args, **kwargs):
        self.stdout.write('Paginating through the MTGSDK to grab card data.')
        self.stdout.write('This could take a while...')
        self._get_all_sets()
        self._update_or_create_set_model_objects()
        self._validate_set_update()
        self._get_all_cards()
        self._change_card_id_release_date_field_names()
        self._update_or_create_card_model_objects()
        self._validate_card_update()
        self._update_or_create_m2m_expansionsetcard_objects()
        self._validate_expansionsetcard_objects()

    def _get_all_sets(self):
        """
        Iterate through MTGSDK and extend all Set objects to self.sets.
        """

        self.sets.extend(Set.all())
        self.stdout.write(f'Grabbed {len(self.sets)} sets.')

    def _update_or_create_set_model_objects(self):
        """
        Loop through SDK Set objects contained in self.sets.
        Create/save a db.models.ExpansionSet object for each SDK Set object.

        If set information already exists in db_card table,
        perform update() instead of create()
        """

        #  Sort all expansions by release date, earliest first.
        self.sets.sort(key=lambda x: x.release_date)

        for expansion in self.sets:
            this_set, created = ExpansionSet.objects.update_or_create(
                code=expansion.code, defaults={**expansion.__dict__}
            )
            if created:
                self.stdout.write(f'CREATED\t{expansion.code}\t{expansion.name}')
            else:
                self.stdout.write(f'UPDATED\t{expansion.code}\t{expansion.name}')

    def _validate_set_update(self):
        """
        Confirm that total sets existing in the MTGSDK API
        matches the total sets existing in the database.
        """

        sdksets_all = len(self.sets)
        sets_all = len(ExpansionSet.objects.all())
        if sdksets_all != sets_all:
            self.stdout.write(self.style.ERROR('***There was a problem.***'))
            self.stdout.write(self.style.ERROR(f'{sdksets_all - sets_all} sets were not inserted into the database.'))
            #Also return set_name, code of missing sets.
        else:
            self.stdout.write(self.style.SUCCESS(f'Update successful. There are now {sets_all} unique sets in the database.'))

    def _get_all_cards(self):
        """
        Paginate through MTGSDK and retrieve all Card objects.

        Upper range limit of 600 will need to be changed as
        more sets/cards are added to the game.
        """

        # What logic to use to check the **actual** last page instead of 600?
        current_page_index = 1
        while True:
        # for i in range(19):
            current_page = SDKCard.where(page=current_page_index).all()
            if len(current_page) == 0:
                return False
            self.cards.extend(current_page)
            self.stdout.write(f'Got page {current_page_index}')
            current_page_index += 1
        self.stdout.write(f'Grabbed {len(self.cards)} cards.')

    def _change_card_id_release_date_field_names(self):
        """
        MTGSDK contains a UUID in a column named 'id' for each card in the SDK.
        This method reassigns the column named 'id' to a column named 'sdk_id'.


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
        the intended functionality of Django's AutoField column 'id'
        which acts as an auto-incrementing primary key.

        This method also populates the Card object's 'release_date' field
        with a datetime.date pulled from the Card's corresponding ExpansionSet.
        """

        count = 0
        for card in self.cards:
            # Change 'id' field to 'sdk_id'
            card.__dict__['sdk_id'] = card.__dict__.pop('id')
            # Adjust Archenemy cards.set from 'OARC' to 'ARC'
            if card.set == 'OARC':
                card.__dict__['set'] = 'ARC'
            # Adjust Archenemy: Nicol Bolas cards.set from 'OE01' to 'E01'
            if card.set == 'OE01':
                card.__dict__['set'] = 'E01'
            # Adjust Planechase cards.set from 'OHOP' to 'HOP'
            if card.set == 'OHOP':
                card.__dict__['set'] = 'HOP'
            # Adjust Planechase 2012 cards.set from 'OPC2' to 'PC2'
            if card.set == 'OPC2':
                card.__dict__['set'] = 'PC2'
            # Adjust Planechase Anthology Planes cards.set from 'OPCA' to 'PCA'
            if card.set == 'OPCA':
                card.__dict__['set'] = 'PCA'
            # Adjust Ravnica Allegiance Promos cards.set from 'PRN' to 'PRNA'
            if card.set == 'PRN':
                card.__dict__['set'] = 'PRNA'
            # Set 'Nalathni Dragon' release_date manually to match 'PDRC' date
            if card.set == 'PRED':
                card.__dict__['release_date'] = '1994-01-01'
                count += 1
            # Populate 'release_date' field with value from corresponding set
            if not card.release_date:
                try:
                    set_release_date = next(
                        set.release_date for set in self.sets if card.set == set.code
                    )
                except:
                    self.errors.append((card.name, card.set, card.set_name))
                    continue
                card.__dict__['release_date'] = set_release_date
                count += 1
        self.stdout.write(f'Changed {count} cards\' \'id\' and \'release_date\' fields.')

    def _update_or_create_card_model_objects(self):
        """
        Loop through SDKCard objects contained in self.cards.
        Create/save a db.models.Card object for each SDKCard object.

        If card information already exists in db_card table,
        perform update() instead of create().
        """

        # Sort all cards by release_date earliest first, then alphabetically.
        self.cards.sort(key=lambda x: (x.release_date, x.set, x.name))

        for card in self.cards:
            this_card, created = Card.objects.update_or_create(
                sdk_id=card.sdk_id,
                defaults={**card.__dict__}
            )
            if created:
                self.stdout.write(f'CREATED\t{this_card.id}\t{this_card.set}\t{this_card.name}')
            else:
                self.stdout.write(f'UPDATED\t{this_card.id}\t{this_card.set}\t{this_card.name}')

    def _validate_card_update(self):
        """
        Confirm that total cards existing in the MTGSDK API
        matches the total cards existing in the database.
        """

        sdkcards_all = len(self.cards)
        cards_all = len(Card.objects.all())
        if sdkcards_all != cards_all:
            self.stdout.write(self.style.ERROR('***There was a problem.***'))
            self.stdout.write(self.style.ERROR(f'{sdkcards_all - cards_all} cards were not inserted into the database.'))
            print(f'There are errors with the following cards: {self.errors}')
            #Also return name, set_name, sdk_id of missing cards.
        else:
            self.stdout.write(self.style.SUCCESS(f'Update successful. There are now {cards_all} unique cards in the database.'))
            print(f'There are errors with the following cards: {self.errors}')

    def _update_or_create_m2m_expansionsetcard_objects(self):
        """
        Update or create ExpansionSetCard object using Card and ExpansionSet
        in a many-to-many relationship.
        """
        all_cards = sorted(
            list(Card.objects.all()),
            key=lambda x: (x.release_date, x.set, x.name)
        )
        for card in all_cards:
            # All cards have a correct 'set' except for Nalathni Dragon. Manual exception.
            try:
                this_cards_set_id = [set.id for set in ExpansionSet.objects.all() if set.code == card.set][0]
            # If card if Nalathni Dragon
            except IndexError:
                this_cards_set_id = 7
            this_expansionset_card, created = ExpansionSetCard.objects.update_or_create(
                card_id=card.id,
                expansionset_id=this_cards_set_id
            )
            if created:
                self.stdout.write(f'CREATED\t{this_expansionset_card.id}\t{this_expansionset_card.card_id}\t{this_expansionset_card.expansionset_id}\t{card.set}\t{card.name}')
            else:
                self.stdout.write(f'UPDATED\t{this_expansionset_card.id}\t{card.set}\t{card.name}')

    def _validate_expansionsetcard_objects(self):
        """
        Confirm that total cards existing in the ExpansionSetCard table
        matches the total cards existing in the Card table.
        """
        expansionsetcards_all = len(ExpansionSetCard.objects.all())
        cards_all = len(Card.objects.all())
        if expansionsetcards_all != cards_all:
            self.stdout.write(self.style.ERROR('***There was a problem.***'))
            self.stdout.write(self.style.ERROR(f'{expansionsetcards_all - cards_all} cards were not inserted into the database.'))
            print(f'There are errors with the following cards: {self.errors}')
            #Also return name, set_name, sdk_id of missing cards.
        else:
            self.stdout.write(self.style.SUCCESS(f'Update successful. There are now {cards_all} ExpansionSetCards in the database.'))
            print(f'There are errors with the following cards: {self.errors}')
