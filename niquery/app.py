from __future__ import unicode_literals

import os
import logging
import argparse

from flask import Flask
from flask import json as json_flask
from flask.wrappers import Request, _missing, _get_data

from niquery.celery_app import make_celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)

@celery.task()
def add_together(a, b):
    return a + b

if __name__ ==  '__main__':
    flask_app.run(debug=True)