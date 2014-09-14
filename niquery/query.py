"""
The query module provides an object to access SPARQL queries over PROV and NIDM
 objects.
"""
__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os
import urlparse

import rdflib

import niquery.utils as utils


class QueryBase(object):
    """
    Base Query class that initializes a graph and provides available sparql
    metadata descriptions.
    """
    def __init__(self, **kwargs):
        self._config = None
        self._graph = self._build_graph(**kwargs)
        self._queries = utils.get_sparql_queries()
        self.sparql_meta = self._get_sparql_meta()

    def _build_graph(self, config=None):
        """
        Builds a rdflib graph base on config with SPARQLStore URIs
        """
        self._config = config
        if self._config:
            sparql_uri = self._config.get('SPARQL_URI')
            update_uri = self._config.get('UPDATE_URI')
            update_usr = self._config.get('UPDATE_USR')
            update_pwd = self._config.get('UPDATE_PWD')
            update_auth = self._config.get('UPDATE_AUTH')
            if sparql_uri and update_uri:
                g = rdflib.ConjunctiveGraph('SPARQLUpdateStore')
                g.open((sparql_uri, update_uri))
                g.store.setCredentials(update_usr, update_pwd)
                g.store.setHTTPAuth(update_auth)
            elif sparql_uri:
                g = rdflib.ConjunctiveGraph('SPARQLStore')
                g.open(sparql_uri)
            else:
                raise Exception("Config must contain SPARQL/UPDATE URIs")
        else:
            g = rdflib.ConjunctiveGraph()
        # Loads the base set of namespaces into rdflib
        for prefix, namespace in utils.NS.iteritems():
            g.bind(prefix, namespace)
        return g

    def _filter_queries(self, ns):
        """
        Enables subclasses to filter queries by type (e.g., SELECT queries are
        filtered using utils.NS.niq.Select.
        """
        select_filter = self.sparql_meta.format == str(ns)
        return self.sparql_meta[select_filter]

    def get_query_string(self, index):
        """
        Extracts the actual query text to execute, based on the query index.
        """
        queries = utils.get_sparql_queries()
        row = self.sparql_meta.ix[index]
        base = os.path.basename(urlparse.urlsplit(row.downloadURL).path)
        return queries[base]

    def _get_sparql_meta(self):
        """
        Parses the query metadata and load a table of available queries.
        """
        self._graph.parse(source=utils.get_meta_path(),
                          publicID=''.join(['file://', utils.get_meta_path()]),
                          format='turtle')
        result = self._graph.query(self._queries['meta.rq'])
        df = utils.result_to_dataframe(result)
        uuid_series = df.uri.str.slice(start=27)
        uuid_series.name = 'uuid'
        uuid = df.join(uuid_series)
        return uuid.set_index('uuid')

    def describe_query(self, index):
        """
        Uses the index of a query to return a description
        """
        return self.sparql_meta.ix[index]

    def execute(self, query_index,
                turtle_file=None, turtle_str=None, turtle_url=None):

        """
        Execute a query stored in `niquery/sparql/` after loading an
        optional graph.

        Note: Each query type provides its own response type (e.g., Pandas
        Dataframe, Boolean, etc.)

        Parameters
        ----------
        query_index : str
        turtle_file : str, optional
        turtle_str : str, optional
        turtle_url : str, optional
        sparql_store : str, optional
        update_store : str, optional

        Returns
        -------
        result : rdflib.plugins.sparql.processor.SPARQLResult
            rdflib SPARQLResult object
        """
        query = self.get_query_string(query_index)
        if turtle_file or turtle_str or turtle_url:
            self._graph.parse(source=turtle_file,
                              data=turtle_str,
                              location=turtle_url,
                              format='turtle')
        result = self._graph.query(query)
        return result

    def get_graph(self):
        """
        Returns the currently loaded graph
        """
        return self._graph


class SelectQuery(QueryBase):
    def __init__(self, **kwargs):
        super(SelectQuery, self).__init__()
        self._graph = self._build_graph(kwargs.get('config'))
        self.sparql_meta = self._filter_queries(utils.NS.niq.Select)

    def execute_select(self, query_index, **kwargs):
        """
        Execute a query, but return dataframe of the results.

        Parameters
        ----------
        query_index : str

        Returns
        -------
        df : pandas.Dataframe
            Dataframe object of SELECT SPARQL query
        """
        result = self.execute(query_index, **kwargs)
        return utils.result_to_dataframe(result)


class AskQuery(QueryBase):
    def __init__(self):
        super(AskQuery, self).__init__()
        self.sparql_meta = self._filter_queries(utils.NS.niq.Ask)

    def execute_ask(self, query_index, **kwargs):
        """
        Execute a query, but only return the boolean response

        Parameters
        ----------
        query_index : str

        Returns
        -------
        result : bool
            Boolean result from ASK SPARQL query
        """
        result = self.execute(query_index, **kwargs)
        return result.askAnswer


