from django.test import TestCase
from db.models import Card, ExpansionSet


class dbUrlsTest(TestCase):

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_card_list(self):
        response = self.client.get('/db/cards/')
        self.assertEqual(response.status_code, 200)

    def test_card_detail(self):
        card = Card.objects.create(
            name='Card 1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        response = self.client.get('/db/card/1-card-1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'card_slug' in response.context['view'].__dict__['kwargs']
        )

    def test_expansion_list(self):
        expansion = ExpansionSet.objects.create(
            id=1,
            code='TS1',
            name='TEST set 1',
        )
        response = self.client.get('/db/expansions/')
        self.assertEqual(response.status_code, 200)

    def test_expansion_detail(self):
        expansion = ExpansionSet.objects.create(
            id=2,
            code='TS2',
            name='TEST set 2',
        )
        response = self.client.get(
            '/db/expansion/test-set-2',
            kwargs={
                'set_slug': expansion.slug
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'set_slug' in response.context['view'].__dict__['kwargs']
        )
