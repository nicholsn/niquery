import json
from flask import Flask, jsonify, request
from flask.ext.restful import Api, Resource

from rdflib import Graph, URIRef, Namespace

app = Flask(__name__)
api = Api(app)


class ROOT(Resource):
    
    def get(self):
        
"""        
        dbo = Namespace('http://dbpedia.org/ontology/')

        graph = Graph(store='SPARQLStore')

        graph.open("http://dbpedia.org/sparql")

        query = u'CONSTRUCT { <http://dbpedia.org/resource/Berlin> <http://dbpedia.org/ontology/populationTotal> ?o } \
                   WHERE { <http://dbpedia.org/resource/Berlin> <http://dbpedia.org/ontology/populationTotal> ?o }'

        result = graph.store.query(query)

        response = json.loads(result.serialize(format='json-ld'))

        return jsonify(response)
"""

api.add_resource(ROOT, '/')

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404,
               'message': 'Not Found: ' + request.url,
               }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == '__main__':
    app.run(debug=True)