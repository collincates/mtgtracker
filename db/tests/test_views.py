from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

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

    def test_card_list_view_has_no_cards(self):
        Card.objects.all().delete()
        response = self.client.get(reverse('card_list'))
        self.assertContains(
            response,
            'No cards are available with these options.'
        )

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


class CardDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # user = get_user_model.objects.create(username='test_user')
        card = Card.objects.create(
            name=f'Test Card',
            set_name='a test set',
            id=1,
            sdk_id='test sdk_id',
        )

    def test_card_detail_view_url_exists_at_desired_location(self):
        card = Card.objects.get(id=1)
        response = self.client.get(card.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_url_accessible_by_name_with_slug_argument(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_contains_custom_slug_field(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse(
            'card_detail',
            kwargs={
                # 'set_slug': slugify(card.set_name),
                'card_slug': card.slug,
            }
        ))

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context[-1]['view'].slug_field, 'slug')

    def test_card_detail_view_contains_custom_slug_url_kwarg(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_url_kwarg, 'slug')

    def test_card_detail_view_card_name_on_detail_page(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, card.name)
        self.assertEqual(response.context['card'].name, 'Test Card')

    def test_card_detail_view_card_sdk_id_on_detail_page(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, card.name)
        self.assertEqual(response.context['card'].sdk_id, 'test sdk_id')
