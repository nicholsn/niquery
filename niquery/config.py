# Celery Configuration
CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'
CELERYD_POOL_RESTARTS = True # Required for /worker/pool/restart API

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'America/Los_Angeles'
CELERY_ENABLE_UTC = True

# Track the status of a task after executed by a worker.
CELERY_TRACK_STARTED = True
CELERY_TASK_RESULT_EXPIRES = 3600

# List of modules to import when celery starts.
#CELERY_IMPORTS = ('api', )

#CELERY_ROUTES = {'proj.tasks.add': {'queue': 'hipri'}}

# Set the queues the worker will consume from
#CELERY_QUEUES =['']