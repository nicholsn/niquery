"""
The query module provides an object to access SPARQL queries over PROV and NI-DM objects.
"""
__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os
import urlparse
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
        self._queries = utils.get_sparql_queries()
        self._bind_prefixes()
        self.sparql_meta = self._get_sparql_meta()

    def _get_sparql_meta(self):
        self._graph.parse(os.path.join(utils.get_meta_path()), format='turtle')
        result = self._graph.query(self._queries['meta.rq'])
        return utils.result_to_dataframe(result)

    def _bind_prefixes(self):
        for prefix, namespace in utils.NS.iteritems():
            self._graph.bind(prefix, namespace)

    def _get_query_string(self, index):
        queries = utils.get_sparql_queries()
        row = self.sparql_meta.iloc[index]
        base = os.path.basename(urlparse.urlsplit(row.downloadURL).path)
        return queries[base]

    def get_graph(self):
        return self._graph

    def describe_query(self, index):
        return self.sparql_meta.iloc[index]


class SelectQuery(QueryBase):
    def __init__(self):
        super(SelectQuery, self).__init__()
        self.sparql_meta = self._filter_queries()

    def _filter_queries(self):
        select_filter = self.sparql_meta.format == str(utils.NS.niq.Select)
        return self.sparql_meta[select_filter]

    def execute(self, query_index, turtle_file=None, turtle_url=None):
        query = self._get_query_string(query_index)
        self._graph.parse(source=turtle_file, location=turtle_url, format='turtle')
        result = self._graph.query(query)
        return utils.result_to_dataframe(result)
