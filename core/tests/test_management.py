from io import StringIO
from django.core.management import call_command
from django.test import TestCase, tag

@tag('slow')
class UpdateDBCardDatabaseTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('update_card_set_database', stdout=out)
        self.assertIn('Update successful', out.getvalue())
