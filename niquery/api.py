from __future__ import absolute_import

from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='amqp://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()