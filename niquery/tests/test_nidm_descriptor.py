__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os
import urlparse
import unittest

import niquery as niq


class DescriptorCase(unittest.TestCase):
    """
    NIDM Dataset Descriptor Validation
    """
    def setUp(self):
        self.turtle = os.path.join(os.path.dirname(__file__),
                                   'data', 'nidm-descriptor.ttl')
        self.select = niq.SelectQuery()

    def test_project_summary_must(self):
        """
        Project Summary-level description that MUST be present.
        """
        test_query = 'B0E44766-B5FD-442B-98D8-993DF49A868C'
        test_filter = self.select.sparql_meta.downloadURL.str.contains(test_query)
        test_record = self.select.sparql_meta[test_filter]
        idx = test_record.index.to_native_types()[0]
        result = self.select.execute_select(idx, turtle_file=self.turtle)
        # check that each of the required elements are present
        self.assertEqual(urlparse.urlparse(result.uri[0]).fragment, "database")
        self.assertEqual(result.title[0], "Database Summary Title")
        self.assertEqual(result.description[0], "Database summary-level description.")
        self.assertEqual(result.type[0], "http://purl.org/dc/dcmitype/Dataset")
        self.assertEqual(result.publisher[0],"https://publisher.org")
        self.assertEqual(urlparse.urlparse(result.hasPart[0]).fragment, "project")


if __name__ == '__main__':
    unittest.main()
