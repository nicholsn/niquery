__author__ = 'Nolan Nichols <orcid.org/0000-0003-1099-3328>'

import unittest

from mock import patch

from niquery.app import flask_app
from niquery.celery_app import make_celery


class MakeCeleryTestCase(unittest.TestCase):

    @patch('niquery.celery_app.Celery')
    def test_make_celery(self, mock_Celery):
        make_celery(flask_app)
        mock_Celery.assert_called_with(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])