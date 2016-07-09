#!/usr/bin/python2
import json
import SPARQLWrapper
import rdflib
from rdflib import Namespace, BNode, Graph, ConjunctiveGraph, Literal, XSD, URIRef
from rdflib.namespace import RDF, FOAF, XSD


def creaGrafoRDF(doc, titolo, capitoli , figure, tabelle): # creo il grafo del documento doc

	doco = Namespace('http://purl.org/spar/doco/')
	po = Namespace('http://www.essepuntato.it/2008/12/pattern#')
	dcterms= Namespace ('http://purl.org/dc/terms/') 
 	fabio = Namespace('http://purl.org/spar/fabio/')
 	co = Namespace('http://purl.org/co/')
 	c4o = Namespace('http://purl.org/spar/c4o')
 	frbr = Namespace('http://purl.org/vocab/frbr/core#')

	doc = doc.replace(" ","")
	doc = doc.replace("_","-")
	uriDoc = Namespace('http://ceur-ws.org/section/vol-'+doc)

	documento = URIRef (uriDoc)

	uriTit = uriDoc+"-title" 

	g = Graph()

	g.add( (documento , RDF.type , fabio.JournalArticle) )

	############################################ TITOLO ###############################################
	g.add( (documento, frbr.part, URIRef(uriTit)) )
	g.add( (URIRef(uriTit) ,RDF.type,  doco.Title))
	g.add( (URIRef(uriTit), c4o.hasContent , Literal(titolo)))

	############################################# CAPITOLI ############################################
	
	i = 1
	for x in capitoli:
		uriCapitolo = uriDoc+"_sec"+str(i) # creo l'uri dei nodi capitoli

		g.add( (documento, frbr.part , URIRef(uriCapitolo) ) )
		g.add( (URIRef(uriCapitolo), RDF.type, doco.Section ))		  

		if '0'<= x[0] <='9':	# creo l'indice dei nodi capitoli
			g.add( (URIRef(uriCapitolo), doco.Index, Literal(x[0], datatype=XSD.integer) ))
			x = x[1:]
		else:
			g.add( (URIRef(uriCapitolo), doco.Index, Literal(i, datatype=XSD.integer) )) 

		while x[0] == " " or x[0] == ".":
			x = x[1:]

		uriSectionTitle =documento+"-sectionTitle"+str(i)  #creo l'uri del nodo titolo del capitolo

		g.add( (URIRef(uriCapitolo),po.containsAsHeader, URIRef(uriSectionTitle)) )
		g.add( (URIRef(uriSectionTitle), RDF.type, doco.SectionTitle))

		g.add( (URIRef(uriSectionTitle), c4o.hasContent , Literal(x)))
		i=i+1

	################################################ FIGURE ###########################################

	i = 1
	for x in figure:
		uriFigura = uriDoc+"_fig"+str(i)   # creo l'uri del nodo figura

		g.add( (documento, frbr.part, URIRef(uriFigura)) )
		g.add( (URIRef(uriFigura), RDF.type, doco.Figure ) )

		g.add( (URIRef(uriFigura), doco.Index, Literal(i, datatype=XSD.integer) ))

		uriTitleFigure = documento+"-TitleFigure"+str(i)   #creo l'uri del nodo titolo della figura

		g.add( (URIRef(uriFigura),po.containsAsHeader, URIRef(uriTitleFigure)) )
		g.add( (URIRef(uriTitleFigure), RDF.type, doco.FigureLabel))
		g.add( (URIRef(uriTitleFigure), c4o.hasContent , Literal(x)) )

		i= i+1

	############################################# TABELLE #############################################

	i = 1
	for x in tabelle:
		uriTabella = uriDoc+"_tab"+str(i)		# creo l'uri del nodo tabella

		g.add( (documento, frbr.part , URIRef(uriTabella)) )
		g.add( (URIRef(uriTabella), RDF.type , doco.Table) )

		g.add( (URIRef(uriTabella), doco.Index, Literal(i, datatype=XSD.integer) ))

		uriTitleTable = documento+"-TitleTable"+str(i)		#creo l'uri del nodo titolo della tabella

		g.add((URIRef(uriTabella), po.containsAsHeader, URIRef(uriTitleTable)))
		g.add((URIRef(uriTitleTable), RDF.type, doco.TableLabel ))
		g.add( (URIRef(uriTitleTable), c4o.hasContent , Literal(x)) )

		i = i+1

	return g