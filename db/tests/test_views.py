from collections import Counter
import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from db.models import Card, ExpansionSet


class CardListViewTest(TestCase):

    def setUp(self):
        # Create 203 cards for pagination tests
        number_of_cards = 203

        for card_id in range(number_of_cards):
            Card.objects.create(
                name=f'Card {card_id}',
                id=f'{card_id}',
                sdk_id=f'{card_id}',
                printings=[card_id]
            )

    def test_card_list_view_url_exists_at_desired_location(self):
        response = self.client.get('/db/cards/')
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('db:card_list'))
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_uses_correct_template(self):
        response = self.client.get(reverse('db:card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'db/card_list.html')

    def test_card_list_view_has_no_cards(self):
        Card.objects.all().delete()
        response = self.client.get(reverse('db:card_list'))
        self.assertContains(
            response,
            'No cards are available with these options.'
        )

    def test_card_list_view_pagination_is_one_hundred(self):
        response = self.client.get(reverse('db:card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 100)

    def test_card_list_view_pagination_lists_all_cards(self):
        response = self.client.get(reverse('db:card_list') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 3)

    def test_card_list_view_ordered_by_name(self):
        response = self.client.get(reverse('db:card_list'))
        sorted_cards = Card.objects.all().order_by('name')
        self.assertEqual(response.context['object_list'][79], sorted_cards[79])

    def test_card_list_get_queryset_filters_only_latest_printings(self):
        card1_bested = Card.objects.create(
            name=f'Bested Behemoth',
            set='ATS',
            set_name='a test set',
            id=204,
            sdk_id='test sdk_id 1',
            release_date='1995-04-05',
            printings=['ATS', 'ATS2']
        )

        card2_bested = Card.objects.create(
            name=f'Bested Behemoth',
            set='ATS2',
            set_name='a test set 2',
            id=205,
            sdk_id='test sdk_id 2',
            release_date='1995-08-05',
            printings=['ATS', 'ATS2']
        )
        card3_abhorrent = Card.objects.create(
            name=f'Abhorrent Behemoth',
            set='ATS',
            set_name='a test set',
            id=206,
            sdk_id='test sdk_id 3',
            release_date='1995-04-05',
            printings=['ATS']
        )

        response = self.client.get(f"{reverse('db:card_list')}?query=behemoth")
        # Queryset should contain card2_bested and card3_abhorrent which are
        # both the most recent printings of cards with 'behemoth' in the title.
        response_queryset = response.context['object_list']
        orm_queryset = Card.objects.filter(id__in=[205, 206]).order_by('name', '-release_date')
        self.assertQuerysetEqual(
            response_queryset,
            orm_queryset,
            transform=lambda x:x
        )

        # Queryset objects should be ordered by 'name', '-release_date'
        self.assertEqual(
            [(card.name, card.release_date) for card in response_queryset],
            [(card.name, card.release_date) for card in orm_queryset]
        )


class CardDetailViewTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            name=f'Test Card',
            set='ATS',
            set_name='a test set',
            id=1,
            sdk_id='test sdk_id',
        )
        self.expansion = ExpansionSet.objects.create(
            id=2,
            code='ATS',
            name='a test set',
            release_date='1993-04-05'
        )
    def test_card_detail_view_url_exists_at_desired_location(self):
        response = self.client.get(self.card.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_url_accessible_by_name_with_slug_argument(self):
        response = self.client.get(reverse('db:card_detail', args=[self.card.slug]))
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_contains_custom_slug_field(self):
        response = self.client.get(reverse(
            'db:card_detail',
            kwargs={
                'card_slug': self.card.slug,
            }
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_field, 'slug')

    def test_card_detail_view_contains_custom_slug_url_kwarg(self):
        response = self.client.get(reverse('db:card_detail', args=[self.card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_url_kwarg, 'slug')

    def test_card_detail_view_card_name_on_detail_page(self):
        response = self.client.get(reverse('db:card_detail', args=[self.card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.card.name)
        self.assertEqual(response.context['card'].name, 'Test Card')

    def test_card_detail_view_card_sdk_id_on_detail_page(self):
        response = self.client.get(reverse('db:card_detail', args=[self.card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.card.name)
        self.assertEqual(response.context['card'].sdk_id, 'test sdk_id')

    def test_card_detail_view_card_set_slug_in_context(self):
        response = self.client.get(reverse('db:card_detail', args=[self.card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.card.slug)
        self.assertEqual(response.context['set_slug'], 'a-test-set')


class ExpansionSetListViewTest(TestCase):

    def setUp(self):
        number_of_sets = 402
        today = datetime.datetime.today()
        # Generate 402 dates in 'YYYY-MM-DD' format, starting from today
        # and incrementing += 1 day per iteration.
        dates = [
            (today + datetime.timedelta(days=x)).date().isoformat() \
            for x in range(0, number_of_sets)
        ]

        for set_id in range(number_of_sets):
            ExpansionSet.objects.create(
                id=f'{set_id}',
                code=f'A{set_id}',
                name=f'Set {set_id}',
                release_date=f'{dates[set_id]}'
            )

    def test_expansionset_list_view_url_exists_at_desired_location(self):
        expansion = ExpansionSet.objects.get(id=23)
        response = self.client.get('/db/expansion/set-23')
        self.assertEqual(response.status_code, 200)

    def test_expansionset_list_view_url_accessible_by_name(self):
        expansion = ExpansionSet.objects.get(id=1)
        response = self.client.get(reverse('db:set_list'))
        self.assertEqual(response.status_code, 200)

    def test_expansionset_list_view_uses_correct_template(self):
        expansion = ExpansionSet.objects.get(id=200)
        response = self.client.get(reverse('db:set_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'db/expansionset_list.html')

    def test_expansionset_list_view_empty_database(self):
        ExpansionSet.objects.all().delete()
        response = self.client.get(reverse('db:set_list'))
        self.assertFalse('object_list' in response.context)

    # def test_expansionset_list_view_with_empty_queryset(self):
    #     self.queryset = None
    #     response = self.client.get(reverse('db:set_list'))
    #     self.assertTrue(len(response.context['object_list'] == 0)

    def test_expansionset_list_view_pagination_is_one_hundred(self):
        response = self.client.get(reverse('db:set_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['expansionset_list']) == 100)

    def test_expansionset_list_view_pagination_lists_all_cards(self):
        response = self.client.get(reverse('db:set_list') + '?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['expansionset_list']) == 2)

    def test_expansionset_list_view_ordered_by_release_date(self):
        response = self.client.get(reverse('db:set_list'))
        sorted_expansionsets = ExpansionSet.objects.all().order_by('release_date')
        self.assertEqual(
            response.context['object_list'][79],
            sorted_expansionsets[79]
        )

class ExpansionSetDetailViewTest(TestCase):

    def setUp(self):
        self.expansion = ExpansionSet.objects.create(
            id=4,
            code='LE4',
            name='Limited Edition 4',
            release_date='1993-04-05'
        )

    def test_expansionset_detail_view_url_exists_at_desired_location(self):
        response = self.client.get(self.expansion.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_expansionset_detail_view_url_accessible_by_name_with_slug_argument(self):
        response = self.client.get(reverse('db:set_detail', args=[self.expansion.slug]))
        self.assertEqual(response.status_code, 200)

    def test_expansionset_detail_view_contains_custom_slug_field(self):
        response = self.client.get(reverse(
            'db:set_detail',
            kwargs={
                'set_slug': self.expansion.slug,
            }
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_field, 'slug')

    def test_expansionset_detail_view_contains_custom_slug_url_kwarg(self):
        response = self.client.get(reverse('db:set_detail', args=[self.expansion.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_url_kwarg, 'slug')

    def test_expansionset_detail_view_set_name_on_detail_page(self):
        response = self.client.get(reverse('db:set_detail', args=[self.expansion.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.expansion.name)
        self.assertEqual(response.context['expansionset'].name, 'Limited Edition 4')

    def test_expansionset_detail_view_set_release_date_on_detail_page(self):
        response = self.client.get(reverse('db:set_detail', args=[self.expansion.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('expansionset' in response.context)
        self.assertEqual(
            response.context['expansionset'].release_date,
            datetime.date(1993, 4, 5)
        )

    def test_expansionset_override_get_context_data_set_cards(self):
        card1 = Card.objects.create(
            name='Card 1',
            set_name='Limited Edition 4',
            id=1,
            sdk_id='123',
            set = 'LE4'
        )
        card2 = Card.objects.create(
            name='Card 2',
            set_name='Limited Edition 4',
            id=2,
            sdk_id='234',
            set = 'LE4'
        )
        response = self.client.get(reverse('db:set_detail', args=[self.expansion.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['set_cards'])
        self.assertEqual(len(response.context['set_cards']), 2)

    def test_expansionset_override_get_context_data_cards_by_color(self):
        self.assertTrue(False)

class ExpansionsetChartDataTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(
            name='Card 1',
            set_name='Limited Edition 4',
            id=1,
            sdk_id='123',
            release_date='1993-04-05',
            color_identity=[]
        )
        self.card2 = Card.objects.create(
            name='Card 2',
            set_name='Limited Edition 4',
            id=2,
            sdk_id='456',
            release_date='1993-04-05',
            color_identity=['W']
        )
        self.card3 = Card.objects.create(
            name='Card 3',
            set_name='Limited Edition 4',
            id=4,
            sdk_id='789',
            release_date='1993-04-05',
            color_identity=['U', 'B']
        )
        self.expansion = ExpansionSet.objects.create(
            id=4,
            code='LE4',
            name='Limited Edition 4',
            release_date='1993-04-05'
        )

    def test_expansionset_chart_data_series_date_parses_correctly(self):
        cards_by_color = Counter()
        # Does this actually test the m2m lookup?
        set_cards = Card.objects.filter(set_name=self.expansion.name)
        for card in set_cards:
            if len(card.color_identity) == 0:
                cards_by_color['colorless'] += 1
            elif len(card.color_identity) == 1:
                cards_by_color[card.color_identity[0]] += 1
            elif len(card.color_identity) > 1:
                cards_by_color['multicolor'] += 1
            else:
                # Is there an else?
                pass
        chart = {
            'chart': {'type': 'column'},
            'title': {'text': 'Card Count by Color Identity'},
            'series': [{
                'name': 'Color Identities',
                'data': [{'name': k, 'y': v} for k, v in cards_by_color.items()]
            }]
        }

        self.assertEqual(
            chart['series'][0]['data'],
            [
                {'name': 'colorless', 'y': 1},
                {'name': 'W', 'y': 1},
                {'name': 'multicolor', 'y': 1}
            ]
        )
