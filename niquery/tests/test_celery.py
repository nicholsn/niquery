__author__ = 'Nolan Nichols <orcid.org/0000-0003-1099-3328>'

from niquery.celery import make_celery

import mock
import unittest


class MakeCeleryTestCase(unittest.TestCase):

    @mock.patch('niquery.Celery')
    def test_make_celery(self, mock_Celery):
        make_celery("Flask App Instance")
        mock_Celery.assert_called_with("Flask App Instance")
