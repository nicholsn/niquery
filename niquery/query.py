"""
The query module provides an object to access SPARQL queries over PROV and NI-DM objects.
"""
__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import StringIO

import rdflib
import requests
import pandas as pd

import utils


class QueryBase(object):
    """
    Base Query class that initializes a graph and provides available sparql metadata descriptions.
    """
    def __init__(self):
        self._graph = rdflib.Graph()
        self._bind_prefixes()
        self.sparql_meta = self._get_sparql_meta()

    def _get_sparql_meta(self):
        sparql_meta = utils.get_sparql_meta_files()
        self._graph.parse(sparql_meta[0], format='turtle')
        with open(sparql_meta[1]) as query:
            result = self._graph.query(query.read())
            meta = StringIO.StringIO(result.serialize(format='csv'))
            return pd.read_csv(meta)

    def _bind_prefixes(self):
        for prefix, namespace in utils.NS.iteritems():
            self._graph.bind(prefix, namespace)

    def get_graph(self):
        return self._graph


class SelectQuery(QueryBase):
    def __init__(self):
        super(SelectQuery, self).__init__()

    def get_queries(self):
        queries = self.sparql_meta
        return queries

    def execute(self, turtle_file, query_url):
        query = requests.get(query_url)
        self._graph.parse(turtle_file, format='turtle')
        result = self._graph.query(query.text)
        return result
