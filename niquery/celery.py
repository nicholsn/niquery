from __future__ import absolute_import

from celery import Celery

app = Celery('niquery',
             broker='redis://',
             backend='redis://',
             include=['niquery.tasks'])

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()