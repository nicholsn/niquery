__author__ = 'Nolan Nichols <orcid.org/0000-0003-1099-3328>'

import unittest

import rdflib
from rdflib.plugins.sparql.processor import SPARQLResult
import pandas as pd
from mock import patch

from niquery.query import QueryBase, SelectQuery, AskQuery


class QueryBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.query = QueryBase()

    def test_init(self):
        self.assertIsInstance(self.query, QueryBase)

    def test_describe_query(self):
        res = self.query.describe_query(1)
        self.assertGreater(len(res), 1)

    def test_execute(self):
        res = self.query.execute(0)
        self.assertIsInstance(res, SPARQLResult)

    def test_get_graph(self):
        self.assertIsInstance(self.query.get_graph(), rdflib.Graph)


class SelectQueryTestCase(unittest.TestCase):

    def setUp(self):
        self.query = SelectQuery()

    def test_init(self):
        self.assertIsInstance(self.query, SelectQuery)
        self.assertGreater(len(self.query.sparql_meta), 0)

    def test_execute_select(self):
        res = self.query.execute_select(0)
        self.assertIsInstance(res, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
