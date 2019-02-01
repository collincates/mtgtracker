from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class UpdateDBCardDatabaseTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_commaned('update_db_card_database', stdout=out)
        self.assertIn('problem', out.getvalue())
