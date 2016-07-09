#!/usr/bin/python2
import csv
import rdflib
import urllib
import urllib2
import codecs
import os

import sys

if len(sys.argv)!= 7 or not (sys.argv[2] == "capitoli" or sys.argv[2]=="figure" or sys.argv[2]=="tabelle" or sys.argv[2]=="all"):
	sys.exit( "Necessari 6 parametri:"+'\n'+"1) indirizzo directory nella quale sono presenti i pdf dei quali si vuole fare l'evaluetion" +'\n'+"2) tipo di valutazione che si vuole fare(capitoli/ figure/ tabelle/all(per farli tutti insieme))"+'\n'+"3) il file di configurazione per i titoli dei file da creare"+'\n'+"4) endpoint della query"+'\n'+"5) l'URI del grafo su quale fare la query"+'\n'+"6) indirizzo directory nella quale inserire i file formato csv di output")

diectory = sys.argv[1]
tipoQuery = sys.argv[2]
endpointQuery = sys.argv[4]
graphURIQuery = sys.argv[5]
directoryOutput = sys.argv[6]
tempQuery = tipoQuery


for file in os.listdir(diectory):
	if file.endswith(".pdf"):

		doc = diectory+'/'+file 
		doc = doc.replace(" ","")

		
		

	count = 1
	i = 0
	tempdoc = doc
	if tempQuery == "all":
		count = 3

	while (i < count):

 
 		if count == 3 and i == 0:
 			tipoQuery = "capitoli"
 			doc = tempdoc

 		if count == 3 and i == 1:
 			tipoQuery ="tabelle"
 			doc = tempdoc

 		if count == 3 and i == 2:
 			tipoQuery ="figure"
 			doc = tempdoc 

 		fileConfig = open(sys.argv[3],"r")	 #apro il file di configurazione che mi servira' per cercare i nomi da dare ai file in formato .csv di output 

		errore = True

		if tipoQuery == "capitoli":					#imposto le variabile per le query in base al tipoQuery scelto
			proprieta = "Section"
			proprieta2 = "SectionTitle"
			docImput = 'Q4.'
			colonne = "section-iri,	"+"section-number,		"+"section-title"
			

		if tipoQuery =="figure":
			proprieta = "Figure"
			proprieta2 = "FigureLabel"
			docImput = 'Q6.'
			colonne = "figure-iri,		"+"figure-number,		"+"figure-caption"


		if tipoQuery == "tabelle":
			proprieta = "Table"
			proprieta2 = "TableLabel"
			docImput = 'Q5.'
			colonne = "table-iri,		"+"table-number,		"+"table-caption"


		doc = doc.replace(" ", "")



		for x in fileConfig: 					#cerco nel file di configurazione il nome del file di output da creare
			if x.find(doc)>-1 and x.find(docImput)>-1:
				pos = x.find(".")
				pos2 = x.find(",")
				docImput = docImput + x[pos+1 : pos2]+".csv"
				errore = False
				break

		fileConfig.close()

		
		if errore :			#se non ho trovato il  nome file nel file di configurazione
			sys.exit("il file"+doc+" non e' presente nel file di configurazione")

			
		doc = doc.replace("/","-")		# serializzo il nome del documento
		doc = doc.replace("_", "-")

		if doc.find('.pdf')>1:
			pos = doc.find('.pdf')
			doc = doc[:pos]

		documento = 'http://ceur-ws.org/section/vol-'+doc

						# creo la query da effettuare 
		sparql =("""

			PREFIX doco: <http://purl.org/spar/doco/>
			PREFIX po: <http://www.essepuntato.it/2008/12/pattern#>
			PREFIX foaf: <http://xmlns.com/foaf/0.1/>
			PREFIX dcterms: <http://purl.org/dc/terms/> 
			PREFIX fabio: <http://purl.org/spar/fabio/> 
			PREFIX co: <http://purl.org/co/> 
			PREFIX c4o: <http://purl.org/spar/c4o> 
			PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
			PREFIX frbr: <http://purl.org/vocab/frbr/core#>

			SELECT ?titolo ?i ?nome		

			WHERE {

			<"""+documento+"""> a fabio:JournalArticle;
				frbr:part ?titolo.

			?titolo a doco:"""+proprieta+""";
				doco:Index ?i;
				po:containsAsHeader ?title.

			?title a doco:"""+proprieta2+""";
				c4o:hasContent ?nome.		
			
			}

			ORDER BY ASC(?i)

			""")	

		# eseguo la query e creo i file di output in formato csv 						
		param = urllib.urlencode({'format': 'text/csv','default-graph-uri': graphURIQuery,'query': sparql})

		endpoint = endpointQuery
		csvdata = urllib2.urlopen(endpoint, param).readlines()

		columns = ['titolo', 'i', 'nome']

		data = [dict(zip(columns, row)) for row in csv.reader(csvdata[1:], dialect ="excel")]


		documento = open(directoryOutput+docImput, 'w')	# apro o creo il file di output nella directory specificata

		documento.write(colonne)
		documento.write('\n')

		for d in data:								# scrivo nel file.csv tutte le triple restituite dalla query
			documento.write("<"+d['titolo']+">,")
			documento.write('\t')
			documento.write('"'+d['i']+'"^^xsd:integer,')
			documento.write('\t')
			documento.write('"'+d['nome']+'"')
			documento.write('\n')

		documento.close()

		i = i+1


print "eseguzione terminata con successo"