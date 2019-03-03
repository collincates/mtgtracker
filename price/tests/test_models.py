from random import choice, randrange

from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from db.models import Card
from price.models import Condition, Price, Vendor


class VendorModelTest(TestCase):

    def setUp(self):
        self.vendor1 = Vendor.objects.create(
            name='FirstVendor',
            code='1ST'
        )
        self.vendor2 = Vendor.objects.create(
            name='SecondVendor',
            code='2ND'
        )

    def test_vendor_meta_verbose_name(self):
        self.assertEqual(Vendor._meta.verbose_name, 'vendor')

    def test_vendor_meta_verbose_name_plural(self):
        self.assertEqual(Vendor._meta.verbose_name_plural, 'vendors')

    def test_vendor_string_representation(self):
        self.assertEqual(self.vendor1.__str__(), self.vendor1.name)


class ConditionModelTest(TestCase):

    def setUp(self):
        self.vendor1 = Vendor.objects.create(
            name='FirstVendor',
            code='1ST'
        )
        self.vendor2 = Vendor.objects.create(
            name='SecondVendor',
            code='2ND'
        )
        self.condition_vendor1_NM = Condition.objects.create(
            vendor=self.vendor1,
            name='Near Mint',
            code='NM'
        )
        self.condition_vendor1_SP = Condition.objects.create(
            vendor=self.vendor1,
            name='Slightly Played',
            code='SP'
        )
        self.condition_vendor1_HP = Condition.objects.create(
            vendor=self.vendor1,
            name='Heavily Played',
            code='HP'
        )
        self.condition_vendor1_DMG = Condition.objects.create(
            vendor=self.vendor1,
            name='Damaged',
            code='DM'
        )
        self.condition_vendor2_NM = Condition.objects.create(
            vendor=self.vendor2,
            name='Near Mint',
            code='NM'
        )
        self.condition_vendor2_LP = Condition.objects.create(
            vendor=self.vendor2,
            name='Lightly Played',
            code='LP'
        )
        self.condition_vendor2_HP = Condition.objects.create(
            vendor=self.vendor2,
            name='Heavily Played',
            code='HP'
        )
        self.condition_vendor2_DMG = Condition.objects.create(
            vendor=self.vendor2,
            name='Damaged',
            code='DMG'
        )

    def test_condition_meta_verbose_name(self):
        self.assertEqual(Condition._meta.verbose_name, 'condition')

    def test_condition_meta_verbose_name_plural(self):
        self.assertEqual(Condition._meta.verbose_name_plural, 'conditions')

    def test_condition_string_representation(self):
        self.assertEqual(
            self.condition_vendor2_LP.__str__(),
            self.condition_vendor2_LP.name
        )

    def test_condition_all_conditions_by_vendor(self):
        self.assertEqual(
            repr(Vendor.objects.get(code='1ST').conditions.all()),
            repr(Condition.objects.filter(vendor=self.vendor1).all())
        )
    def test_condition_all_vendors_for_given_condition(self):
        self.assertEqual(
            repr([Condition.objects.filter(vendor=self.vendor2)]),
            repr([Vendor.objects.get(code='2ND').conditions.all()])
        )

class PriceModelTest(TestCase):

    def setUp(self):
        self.card1 = Card.objects.create(
            name='Card 1',
            set='AT1',
            set_name='a test set',
            sdk_id='123'
        )
        self.card2 = Card.objects.create(
            name='Card 2',
            set='AT2',
            set_name='a test set',
            sdk_id='223'
        )
        self.vendor1 = Vendor.objects.create(
            name='FirstVendor',
            code='1ST'
        )
        self.vendor2 = Vendor.objects.create(
            name='SecondVendor',
            code='2ND'
        )
        self.condition_vendor1_NM = Condition.objects.create(
            vendor=self.vendor1,
            name='Near Mint',
            code='NM'
        )
        self.condition_vendor1_SP = Condition.objects.create(
            vendor=self.vendor1,
            name='Slightly Played',
            code='SP'
        )
        self.condition_vendor2_NM = Condition.objects.create(
            vendor=self.vendor2,
            name='Near Mint',
            code='NM'
        )
        self.condition_vendor2_LP = Condition.objects.create(
            vendor=self.vendor2,
            name='Lightly Played',
            code='LP'
        )

        number_of_prices_per_vendor = 100

        for price in range(number_of_prices_per_vendor):
            Price.objects.create(
                card=choice([self.card1, self.card2]),
                vendor=self.vendor1,
                condition=choice([
                    self.condition_vendor1_NM,
                    self.condition_vendor1_SP
                ]),
                timestamp=timezone.now(),
                qty_in_stock=randrange(0, 20),
                price='{:0.2f}'.format(randrange(0, 100)),
            )
            Price.objects.create(
                card=choice([self.card1, self.card2]),
                vendor=self.vendor2,
                condition=choice([
                    self.condition_vendor2_NM,
                    self.condition_vendor2_LP
                ]),
                timestamp=timezone.now(),
                qty_in_stock=randrange(0, 20),
                price='{:0.2f}'.format(randrange(1, 100)),
            )
        Price.objects.filter(qty_in_stock=0).update(price=None)

    def test_price_unique_together_prevents_duplicates(self):
        random_price = Price.objects.filter(card=self.card2)[50]
        with self.assertRaises(IntegrityError):
            Price.objects.create(
                card=random_price.card,
                vendor=random_price.vendor,
                condition=random_price.condition,
                timestamp=random_price.timestamp,
                qty_in_stock=5,
                price='1.00'
            )

    def test_price_meta_verbose_name(self):
        self.assertEqual(Price._meta.verbose_name, 'price')

    def test_price_meta_verbose_name_plural(self):
        self.assertEqual(Price._meta.verbose_name_plural, 'prices')

    def test_price_string_representation(self):
        random_price = Price.objects.filter(vendor=self.vendor1)[0]
        self.assertEqual(
            random_price.__str__(),
            str(random_price.price)
        )

    def test_price_all_test_prices_are_created(self):
        # 100 prices per vendor are created in this TestCase.
        # We have 2 test vendors, so we should have 200 total prices.
        self.assertEqual(Price.objects.all().count(), 200)

    def test_price_zero_qty_in_stock_has_none_in_price_field(self):
        out_of_stock_items = Price.objects.filter(qty_in_stock=0)
        for item in out_of_stock_items:
            self.assertTrue(item.price == None)

    def test_price_get_all_prices_for_given_card(self):
        self.assertEqual(
            repr([Price.objects.filter(card=self.card1)]),
            repr([Card.objects.get(name='Card 1').prices.all()])
        )

    def test_price_get_all_prices_for_given_vendor(self):
        self.assertEqual(
            repr([Price.objects.filter(vendor=self.vendor2)]),
            repr([Vendor.objects.get(name='SecondVendor').prices.all()])
        )

    def test_price_get_all_prices_for_given_condition(self):
        self.assertEqual(
            repr([Price.objects.filter(condition=self.condition_vendor1_SP)]),
            repr([Condition.objects.get(name='Slightly Played').prices.all()])
        )
