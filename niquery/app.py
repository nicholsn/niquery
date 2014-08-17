from __future__ import unicode_literals, absolute_import

import os
import sys

from flask import Flask, jsonify, request

from niquery.celery_app import make_celery

flask_app = Flask(__name__)

flask_app.config.from_object('niquery.config')

# docker containers use rabbitmq DB link
if os.environ.get('DB_PORT_5672_TCP_ADDR'):
    host = os.environ.get('DB_PORT_5672_TCP_ADDR', None)
    port = os.environ.get('DB_PORT_5672_TCP_PORT', None)
    broker = "amqp://{0}:{1}//".format(host, port)
    flask_app.config.update(CELERY_BROKER_URL=broker,
                            CELERY_RESULT_BACKEND=broker)

celery = make_celery(flask_app)


@celery.task(name="tasks.add")
def add(x, y):
    return x + y


@flask_app.route("/test")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    res = add.apply_async((x, y))
    context = {"id": res.task_id, "x": x, "y": y}
    result = "add((x){}, (y){})".format(context['x'], context['y'])
    goto = "{}".format(context['id'])
    return jsonify(result=result, goto=goto)


@flask_app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)


def main(broker=None):
    if broker:
        flask_app.config.update(CELERY_BROKER_URL=broker,
                                CELERY_RESULT_BACKEND=broker, )
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    sys.exit(main())