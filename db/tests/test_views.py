from django.test import TestCase
from django.urls import reverse

from db.models import Card


class CardListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 203 cards for pagination tests
        number_of_cards = 203

        for card_id in range(number_of_cards):
            Card.objects.create(
                name=f'Card {card_id}',
                id=f'{card_id}',
                sdk_id=f'{card_id}',
            )

    def test_card_list_view_url_exists_at_desired_location(self):
        response = self.client.get('/db/cards/')
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_uses_correct_template(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'db/card_list.html')

    def test_card_list_view_pagination_is_one_hundred(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 100)

    def test_card_list_view_pagination_lists_all_cards(self):
        response = self.client.get(reverse('card_list') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 3)
