from django.test import TestCase

from db.models import Card


class CardModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        card1 = Card.objects.create(name='Card 1', set_name='a test set', id=1, sdk_id='123')
        card2 = Card.objects.create(name='Card 2', set_name='a test set', id=2, sdk_id='456')
        card3 = Card.objects.create(
            name='Card 3',
            set_name='a test set',
            id=3,
            sdk_id='789',
            variations=[card1.sdk_id, card2.sdk_id]
        )

    def test_card_meta_verbose_name(self):
        self.assertEqual(Card._meta.verbose_name, 'card')

    def test_card_meta_verbose_name_plural(self):
        self.assertEqual(Card._meta.verbose_name_plural, 'cards')

    def test_card_meta_ordering_by_id(self):
        results = Card.objects.all()
        self.assertEqual(results[0].name, 'Card 1')
        self.assertEqual(results[1].name, 'Card 2')

    def test_card_string_representation(self):
        card = Card.objects.get(id=1)
        self.assertEqual(str(card), card.name)

    def test_card_override_save_with_slug(self):
        # Card class comes with a blank slug upon instantiation by default.
        card = Card(name='MY test Card', id=234)
        # Assert SlugField contains default blank value.
        self.assertEqual(card.slug, '')
        # .save() is overriden to call slugify(f'{card.id}-{card.name}')
        card.save()
        self.assertEqual(card.slug, '234-my-test-card')

    def test_card_get_absolute_url(self):
        card = Card.objects.get(id=1)
        self.assertEqual(card.get_absolute_url(), '/db/a-test-set/1-card-1')

    def test_card_art_variations(self):
        card3 = Card.objects.get(id=3)
        self.assertQuerysetEqual(
            card3.art_variations(),
            map(repr, ['1-card-1', '2-card-2', '3-card-3'])
        )
