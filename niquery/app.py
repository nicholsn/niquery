from __future__ import unicode_literals, absolute_import

import os
import sys

from flask import Flask, jsonify, request

from niquery.celery_app import make_celery
from niquery.api import api_v1, api_v1_bp, API_VERSION_V1


def create_app(environment=None):
    """
    Creates and configures the app depending on the environment indicated, which can be
    set explicitly or using the FLASK_CONFIG environment variable.

    Environments
    ------------
     - config
     - development (default)
     - production
     - docker
     - testing
    """
    app = Flask(__name__)

    if not environment:
        environment = os.environ.get('FLASK_CONFIG')
    if not environment:
        environment = 'development'

    app.config.from_object(
        'niquery.config.{}'.format(environment.capitalize()))

    # register version 1 of the api
    app.register_blueprint(
        api_v1_bp,
        url_prefix='{prefix}/v{version}'.format(
            prefix=app.config['URL_PREFIX'],
            version=API_VERSION_V1))
    return app

app = create_app()
celery = make_celery(app)

@celery.task(name="tasks.add")
def add(x, y):
    return x + y


@app.route("/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)


@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)


def main(broker=None):
    if broker:
        app.config.update(CELERY_BROKER_URL=broker,
                                CELERY_RESULT_BACKEND=broker, )
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    sys.exit(main())