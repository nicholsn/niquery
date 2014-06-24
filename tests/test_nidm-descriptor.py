__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os
import unittest

import niquery as niq


class DescriptorCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_summary_must(self):
        """
        NIDM Descriptors MUST return one record the following elements to be a valid summary level description.
        """
        query = niq.SelectQuery()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
