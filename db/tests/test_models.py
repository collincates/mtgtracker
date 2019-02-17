# from django.conf import settings
from django.test import TestCase

from accounts.models import User
from db.models import Card, ExpansionSet


class CardModelTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(
            name='Card 1',
            set='AT1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        self.card2 = Card.objects.create(
            name='Card 2',
            set='AT2',
            set_name='a test set 2',
            id=2,
            sdk_id='456'
        )
        self.card3 = Card.objects.create(
            name='Card 3',
            set='AT3',
            set_name='a test set 3',
            id=3,
            sdk_id='789',
            variations=[self.card1.sdk_id, self.card2.sdk_id],
            printings=['AT3', 'AT4', 'AT5']
        )
        self.card3_set_AT4 = Card.objects.create(
            name='Card 3',
            set='AT4',
            set_name='a test set 4',
            id=4,
            sdk_id='101',
            printings=['AT3', 'AT4', 'AT5']
        )
        self.card3_set_AT5 = Card.objects.create(
            name='Card 3',
            set='AT5',
            set_name='a test set 5',
            id=5,
            sdk_id='112',
            printings=['AT3', 'AT4', 'AT5']
        )

    def test_card_meta_verbose_name(self):
        self.assertEqual(Card._meta.verbose_name, 'card')

    def test_card_meta_verbose_name_plural(self):
        self.assertEqual(Card._meta.verbose_name_plural, 'cards')

    def test_card_meta_ordering_by_name(self):
        results = Card.objects.all()
        self.assertEqual(results[0].name, 'Card 1')
        self.assertEqual(results[1].name, 'Card 2')
        self.assertEqual(results[2].name, 'Card 3')

    def test_card_string_representation(self):
        self.assertEqual(self.card1.__str__(), self.card1.name)

    def test_card_override_save_with_slug(self):
        # Card class comes with a blank slug upon instantiation by default.
        card = Card(name='MY test Card', id=234)
        # Assert SlugField contains default blank value.
        self.assertEqual(card.slug, '')
        # .save() is overriden to call slugify(f'{card.id}-{card.name}')
        card.save()
        self.assertEqual(card.slug, '234-my-test-card')

    def test_card_get_absolute_url(self):
        # card = Card.objects.get(id=1)
        card_abs_url = self.card1.get_absolute_url()
        self.assertEqual(card_abs_url, '/db/card/1-card-1')

    def test_card_art_variations(self):
        art_var = self.card3.art_variations()
        self.assertQuerysetEqual(
            art_var,
            map(repr, ['1-card-1', '2-card-2', '3-card-3'])
        )

    def test_card_all_printings(self):
        all_sets = self.card3.all_printings()
        self.assertQuerysetEqual(
            all_sets,
            ['<Card: Card 3>', '<Card: Card 3>', '<Card: Card 3>']
        )

    def test_card_other_printings(self):
        all_sets = self.card3.other_printings()
        self.assertQuerysetEqual(
            all_sets,
            ['<Card: Card 3>', '<Card: Card 3>']
        )


class ExpansionSetModelTest(TestCase):

    def setUp(self):
        self.alpha = ExpansionSet.objects.create(
            name='Limited Edition Alpha',
            code='LEA',
            id=1,
            release_date='1993-08-05',
            )
        self.beta = ExpansionSet.objects.create(
            name='Limited Edition Beta',
            code='LEB',
            id=2,
            release_date='1993-10-04',
            )
        self.unlimited = ExpansionSet.objects.create(
            name='Unlimited Edition',
            code='2ED',
            id=3,
            release_date='1993-12-01',
        )

    def test_expansionset_meta_ordering_by_name(self):
        results = ExpansionSet.objects.all()
        self.assertEqual(results[0].name, 'Limited Edition Alpha')
        self.assertEqual(results[1].name, 'Limited Edition Beta')
        self.assertEqual(results[2].name, 'Unlimited Edition')

    def test_expansionset_meta_verbose_name(self):
        self.assertEqual(ExpansionSet._meta.verbose_name, 'set')

    def test_expansionset_meta_verbose_name_plural(self):
        self.assertEqual(ExpansionSet._meta.verbose_name_plural, 'sets')

    def test_expansionset_string_representation(self):
        self.assertEqual(self.alpha.__str__(), self.alpha.name)

    def test_expansionset_override_save_with_slug(self):
        # ExpansionSet class comes with a blank slug upon instantiation.
        expansionset = ExpansionSet(name='Test Expansion Set', id=4)
        # Assert SlugField contains default blank value.
        self.assertEqual(expansionset.slug, '')
        # .save() is overriden to call slugify(f'{expansionset.name}')
        expansionset.save()
        self.assertEqual(expansionset.slug, 'test-expansion-set')

    def test_expansionset_get_absolute_url(self):
        expansionset_abs_url = self.unlimited.get_absolute_url()
        self.assertEqual(expansionset_abs_url, '/db/expansion/unlimited-edition')
