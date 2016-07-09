#!/usr/bin/python2
from rdflib import ConjunctiveGraph
import json


def post(g, URLendpoint, graphURI):		# eseguo la post del grafo g nel database specificato

	output = {	'risposta': [] }

	endpoint = ConjunctiveGraph ('SPARQLUpdateStore')
	endpoint.open(URLendpoint)
	enddata = """INSERT DATA { 
	                GRAPH <"""+graphURI+"""> {
	                    %s
	                }
	        }""" % g.serialize(format="nt")

	endpoint.update(enddata)
	output['risposta'].append(g.serialize(format="turtle"))
