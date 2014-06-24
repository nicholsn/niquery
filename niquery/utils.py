__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os

import rdflib


# Access namespace objects as attributes
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# available namespaces
NS = AttrDict(nidm=rdflib.Namespace("http://www.incf.org/ns/nidash/nidm#"),
              niq=rdflib.Namespace("http://purl.org/niquery#"),
              prov=rdflib.Namespace("http://www.w3.org/ns/prov#"))

_sparql_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sparql')


def get_sparql_meta_files():
    ttl = os.path.join(_sparql_path, 'meta.ttl')
    rq = os.path.join(_sparql_path, 'meta.rq')
    return ttl, rq


def get_sparql_queries():
    queries = dict()
    for rq_file in os.listdir(_sparql_path):
        if rq_file.endswith('.rq'):
            rq_path = os.path.join(_sparql_path, rq_file)
            with open(rq_path) as rq:
                queries.update({rq_file: rq.read()})
    return queries