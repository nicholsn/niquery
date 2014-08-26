from __future__ import absolute_import

import os
import json

import rdflib
import requests
from celery import Celery
from flask import Flask, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse

from niquery.query import AskQuery


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

    return app


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = create_app()
api = Api(app)

@api.representation('text/turtle')
def turtle(data, code, headers=None):
    g = rdflib.ConjunctiveGraph()  # json-ld parsing works with conjunctive
    g.parse(data=json.dumps(data), format='json-ld')
    resp = make_response(g.serialize(format='turtle'), code)
    resp.headers.extend(headers or {})
    return resp

celery = make_celery(app)

@celery.task(name="tasks.add")
def add(x, y):
    return x + y

@celery.task(name='tasks.bet')
def bet(in_file_uri):
    import nipype
    from nipype.interfaces.fsl import BET

    nipype.config.enable_provenance()

    os.chdir('/tmp')
    fname = 'anatomy.nii.gz'

    with open(fname, 'wb') as fd:
        response = requests.get(in_file_uri, stream=True)
        if not response.ok:
            response.raise_for_status()
        for chunk in response.iter_content(1024):
            fd.write(chunk)

    better = BET()
    better.inputs.in_file = os.path.abspath(fname)
    result = better.run()
    return result.provenance.rdf().serialize(format='json-ld')

parser = reqparse.RequestParser()


class Validate(Resource):
    def get(self):
        ask = AskQuery()
        return ask.sparql_meta.to_dict(outtype='records')


class ValidateResult(Resource):
    def get(self, task_id):
        retval = add.AsyncResult(task_id).get(timeout=1.0)
        return repr(retval)


class Inference(Resource):
    def get(self):
        x = 5
        y = 10
        res = add.apply_async([x, y])
        context = {"id": res.task_id, "x": x, "y": y}
        result = "add((x){}, (y){})".format(context['x'], context['y'])
        goto = "{}".format(context['id'])
        return jsonify(result=result, goto=goto)


class InferenceResult(Resource):
    def get(self, task_id):
        retval = add.AsyncResult(task_id).get(timeout=1.0)
        return repr(retval)


class Compute(Resource):
    def get(self):
        in_file_uri = "http://openfmri.s3.amazonaws.com/ds001/sub001/anatomy/highres001.nii.gz"
        res = bet.apply_async([in_file_uri])
        result = {"task_id": res.task_id, "task": "Run FSL BET", "in_file_uri": in_file_uri}
        return jsonify(result=result)


class ComputeResult(Resource):
    def get(self, task_id):
        async = bet.AsyncResult(task_id)
        result = {'task_id': async.id,
                  'task_state': async.state}
        if async.ready():
            prov = async.get(timeout=1.0)
            result.update({'@graph': json.loads(prov)})
        return result

# Endpoints
api.add_resource(Validate, '/validate')
api.add_resource(ValidateResult, '/validate/<string:task_id>')
api.add_resource(Inference, '/inference')
api.add_resource(InferenceResult, '/inference/<string:task_id>')
api.add_resource(Compute, '/compute', '/compute/')
api.add_resource(ComputeResult, '/compute/<string:task_id>')

if __name__ == "__main__":

    app.run(host=app.config['HOST'], port=app.config['PORT'])

# TODO: 'Validate' NIDM API (Dataset Descriptor)
# TODO: Infer NIDM from XNAT + EXCEL (Experiment)
# TODO: Compute from NIDM (Workflow + Results)