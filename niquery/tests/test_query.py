__author__ = 'Nolan Nichols <orcid.org/0000-0003-1099-3328>'

import unittest

import rdflib
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

    def test_get_graph(self):
        self.assertIsInstance(self.query.get_graph(), rdflib.Graph)



if __name__ == '__main__':
    unittest.main()
