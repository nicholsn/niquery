__author__ = 'Nolan Nichols <http://orcid.org/0000-0003-1099-3328>'

import os


def get_sparql_meta():
    ttl = os.path.join(os.path.dirname(__file__), 'sparql', 'meta.ttl')
    rq = os.path.join(os.path.dirname(__file__), 'sparql', 'meta.rq')
    return ttl, rq
