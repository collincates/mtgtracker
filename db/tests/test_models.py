from django.test import TestCase

from db.models import Card


class CardModelTest(TestCase):

    def test_card_meta_verbose_name(self):
        self.assertEqual(Card._meta.verbose_name, 'card')

    def test_card_meta_verbose_name_plural(self):
        self.assertEqual(Card._meta.verbose_name_plural, 'cards')

    def test_card_meta_ordering_by_id(self):
        card1 = Card.objects.create(name='Card 1', id=1, sdk_id='123')
        card2 = Card.objects.create(name='Card 2', id=2, sdk_id='456')
        results = Card.objects.all()
        self.assertEqual(results[0].name, 'Card 1')
        self.assertEqual(results[1].name, 'Card 2')

    def test_card_string_representation(self):
        card = Card(name='My Test Card')
        self.assertEqual(str(card), card.name)

    def test_card_override_save_with_slug(self):
        # Instantiate Card without a unique slug.
        card = Card(name='MY test Card', id=234)
        # SlugField has blank=True by default.
        self.assertEqual(card.slug, '')
        # .save() overriden to call slugify(f'{card.id}-{card.name}')
        card.save()
        self.assertEqual(card.slug, '234-my-test-card')

    def test_card_get_absolute_url(self):
        pass
