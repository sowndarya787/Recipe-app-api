from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    @patch('time.sleep')
    def test_wait_for_db(self, patched_sleep):
        """Test waiting for db - retries before success"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]

            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 6)

    def test_wait_for_db_ready(self):
        """Test DB is ready and does not wait"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True

            call_command('wait_for_db')

            gi.assert_called_once_with('default')
