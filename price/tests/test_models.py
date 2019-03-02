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
        self.assertQuerysetEqual(
            Vendor.objects.get(id=1).conditions.all(),
            Condition.objects.filter(vendor=self.vendor1)
        )
