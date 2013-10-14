"""
The query module provides a collection of SPARQL queries over PROV and NI-DM objects.
"""

__author__ = 'Nolan Nichols <nolan.nichols@gmail.com'

from rdflib import Graph, Namespace, RDF

PROV = Namespace("http://www.w3.org/ns/prov#")
NIDM = Namespace("http://nidm.nidash.org/")

g = Graph(store="SPARQLStore")

# bind namespace prefixes to the graph
g.bind('prov', PROV)
g.bind('nidm', NIDM)

g.subjects(RDF.type, PROV.Entity)

Entities = 'CONSTRUCT {?subject a prov:Entity .} WHERE {?subject a prov:Entity .}'

Activities = 'CONSTRUCT {?subject a prov:Activity .} WHERE {?subject a prov:Activity .}'

Agents = 'CONSTRUCT {?subject a prov:Agent .} WHERE {?subject a prov:Agent .}'

Projects = 'CONSTRUCT {?subject a nidm:Project .} WHERE {?subject a nidm:Project .}'

Participants = 'CONSTRUCT {?subject a prov:Person .} WHERE {?subject a nidm:Participant . ?subject prov:Role nidm:Participant?}'

Acquisitions = PREFIXES + 'CONSTRUCT {?subject a nidm:Acquisition .} WHERE {?subject a nidm:Acquisition .}'
