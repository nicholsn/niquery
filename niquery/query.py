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

    def _bind_prefixes(self):
        """
        Loads the base set of namespaces into rdflib
        """
        for prefix, namespace in utils.NS.iteritems():
            self._graph.bind(prefix, namespace)

    def _filter_queries(self, ns):
        """
        Enables subclasses to filter queries by type (e.g., SELECT queries are
        filtered using utils.NS.niq.Select.
        """
        select_filter = self.sparql_meta.format == str(ns)
        return self.sparql_meta[select_filter]

    def _get_query_string(self, index):
        """
        Extracts the actual query text to execute, based on the query index.
        """
        queries = utils.get_sparql_queries()
        row = self.sparql_meta.iloc[index]
        base = os.path.basename(urlparse.urlsplit(row.downloadURL).path)
        return queries[base]

    def _get_sparql_meta(self):
        """
        Parses the query metadata and load a table of available queries.
        """
        self._graph.parse(os.path.join(utils.get_meta_path()),
                          format='turtle')
        result = self._graph.query(self._queries['meta.rq'])
        return utils.result_to_dataframe(result)

    def describe_query(self, index):
        """
        Uses the index of a query to return a description
        """
        return self.sparql_meta.iloc[index]

    def execute(self, query_index, turtle_file=None, turtle_url=None):
        """
        Execute a query using the index

        Subclasses define specific parameters and returns
        """
        pass

    def get_graph(self):
        """
        Returns the currently loaded graph
        """
        return self._graph


class SelectQuery(QueryBase):
    def __init__(self):
        super(SelectQuery, self).__init__()
        self.sparql_meta = self._filter_queries(utils.NS.niq.Select)

    def execute(self, query_index, turtle_file=None, turtle_url=None):
        """
        Execute a query using the index

        Parameters
        ----------
        query_index : int
        turtle_file : str, optional
        turtle)url : string, optional

        Returns
        -------
        df : pandas.Dataframe
            Dataframe object of SELECT SPARQL query
        """
        query = self._get_query_string(query_index)
        self._graph.parse(source=turtle_file,
                          location=turtle_url,
                          format='turtle')
        result = self._graph.query(query)
        return utils.result_to_dataframe(result)


class AskQuery(QueryBase):
    def __init__(self):
        super(AskQuery, self).__init__()

