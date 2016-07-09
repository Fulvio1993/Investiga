#!/usr/bin/python2

import os
import sys
import re

import creazione_grafo
import my_post
import creazione_risultati
import inserisci_spazi
import creazione_outfileXML
import ricercaPDF
import ricercaFigureTabelle

reload(sys)
sys.setdefaultencoding('utf-8')
		
if len(sys.argv)<5 or not(sys.argv[3]=="-graph" or sys.argv[3]=="-rdf") or (sys.argv[3] == "-graph" and len(sys.argv)!= 6) or (sys.argv[3] =="-rdf" and len(sys.argv)!= 5):
	sys.exit( "Necessari 5/6 parametri:"+'\n'+"1) nome directory contenente i file pdf da esaminare"+'\n'+"2) indirizzo della cartella nella quale inserire i documenti XML"+'\n'+"3) -graph se si vuole creare un dataset su rdf dei risultati o -rdf se invece si vuole creare un file di testo con i risultati"+'\n'+"4) nome directory nella quale inserire i risultati se si e scelto -rdf o url endpoint e uri grafo nei quali eseguire la post se si e scelto -graph")


directoryInput = sys.argv[1]
directoryOutfile = sys.argv[2]
graphOrRdf = sys.argv[3]
if sys.argv[3] =="-rdf":
	directoryOutput = sys.argv[4]
else:
	URLendpoint = sys.argv[4]
	graphURI = sys.argv[5]

DOCUMENTI = []
primoDocumento = True


for file in os.listdir(directoryInput):			# per ogni file in formato pdf presente nella directory di imput
	if file.endswith(".pdf"):

		doc = directoryInput+'/'+file 
		doc = doc.replace(" ","")

		print "file in esecuzione: "+doc 
		
	doc = creazione_outfileXML.trasformaPDFinXML(doc, directoryOutfile)		# trasformo il file pdf in xml grazie a PDFMiner
	
	############################################################################################################

	documento = open(directoryOutfile+"/"+doc, "r")			#apro il file XML
	 
	stringaNumero = 0
	nStringa = 0
	dimensioneTitolo = 0
	dimensioneCapitolo = 0
	dimensioneLettera = 0
	differenzaBbox= 0
	spazi = 0
	spazi2 = 0
	diffSpazi = 0
	precSpazi = 0
	Bbox = 0
	Bbox2 = 0
	colonne = 0
	altezza = 0
	precAltezza = 0
	h1 = 0
	h2 = 0
	pagina = 0

	lettera = ""
	precLettera = ""
	fontStringa = "" 
	fontTitolo = ""
	fontCapitolo = ""
	PDFrigaPerRiga = ""
	Titolo = ""
	Capitolo =""

	CAPITOLI = []
	FIGURE = []
	TABELLE = []
	FigureDaCercare = []
	PDFrigaPerRigaArray = []
	paginePDF = []
	stringa = []

	Times = False
	primo = True
	Nimbus = False
	Upper = False
	primaH = True
	primaPagina = True
	bordo = False


	font = re.compile(r"""(											#FONT 
					[font="]\w+\s*[+]*\w*\s*\w*\s*[,-]*\w+ ["]
				)""", re.VERBOSE)


	dim = re.compile (r"""(										#DIMENSIONE
					[size="][0-9]{1,2}[.]\d+[">]
				)""", re.VERBOSE)


	bbox = re.compile (r"""(									#BBOX
					[bbox="][0-9]{2,3}[.][0-9]{3}
				)""",re.VERBOSE)



	tabellaBbox = re.compile(r"""(
					[,][0-9]{2,3}[.][0-9]{2,3}["]
				)""", re.VERBOSE)


	altezza1 = re.compile(r"""(
					[,][0-9]{2,3}[.][0-9]{3}[,]
				)""", re.VERBOSE)


	for string in documento:					# inizio ciclo riga per riga del documento xml #########

		stringaNumero = stringaNumero +1

		###################################### RICERCA DIMENSIONE ################################

		searchSize = dim.search(string)

		if searchSize:
			dimensioneLettera = searchSize.group().strip('"')

		#################################### RICERCA FONT ################################

		Font = font.search(string)
		if Font:
			fontStringa =  Font.group().strip('"')

			if stringaNumero == 4:
				dimensioneTitolo = dimensioneLettera

		##################################### 1 O 2 COLONNE? ###################################

		if stringaNumero == 4:
			colonne = bbox.search(string)

			if colonne:
				colonne = int(round(float(colonne.group().strip('"'))))		# se il font e' gia' spaziato Times = True
			if fontStringa.find('Times')>-1 or fontStringa.find("Helvetica")>-1 :
					Times = True

			if fontStringa.find("NimbusSanL")>-1:				# font tutto maiuscolo per i capitoli
				Nimbus = True

			##################################### RICERCA CARATTERE ##############################

		numLiteral = string.find("</t")
		if  numLiteral-6 == string.find(">"):
			lettera = string[string.find(">")+1:string.find("</t")].encode("utf-8")
			if lettera == '&amp;':
				lettera = " &"
			else:
				lettera = ""

		elif (numLiteral > 0 ):
			lettera = string[numLiteral -1]
		else :
			lettera =""

		if 'A'<= precLettera <='Z' and 'A' <= lettera <='Z': 
			Upper =True 				 # se e maiuscola sia la lettera corrente che la precedente

		else :
			Upper = False


		######################################## RICERCA SPAZI #######################################

		spazi = bbox.search(string)
		if spazi:
			spazi2 = spazi.group().strip('"')
			diffSpazi = float(spazi2)-float(precSpazi)		#spazio tra la lettera corrente e la precedente

		######################################### crea PDF riga per riga ########################################

		Bbox = tabellaBbox.search(string)
		if Bbox:
			Bbox2 = Bbox.group().strip(",").strip('"')

		# ricreo il PDF riga per riga e pagina per pagina
		if string.find("page ")>-1:
			pagina = pagina +1
			
			if primaPagina == False:
				stringa = [PDFrigaPerRiga ,precAltezza]
				PDFrigaPerRigaArray +=[stringa]
				paginePDF +=[PDFrigaPerRigaArray]
				PDFrigaPerRigaArray =[]
				PDFrigaPerRiga = ""

			PDFrigaPerRiga =PDFrigaPerRiga +'\n\n'+" pagina "+str(pagina)+'\n\n'
			primaPagina =False

		h1 = altezza1.search(string)		#trovo la posizione nel pdf tramite i bbox
		if h1:
			h2 = h1.group().strip(',')

		if string.find("linewidth")>-1:		#se trovo un bordo bordo = True
			bordo = True

		altezza = int(round(float(h2)))  

		if Times == False:
			PDFrigaPerRiga = inserisci_spazi.Figura(PDFrigaPerRiga, lettera, precLettera, diffSpazi)

		if str(altezza) ==  str(precAltezza):		#se sono sulla stessa altezza nel PDF
			if primaH :
				PDFrigaPerRiga = PDFrigaPerRiga + precLettera +lettera
				primaH = False

			else:
				PDFrigaPerRiga = PDFrigaPerRiga +lettera

		else :
			differenzaBbox = float(precBbox)-float(Bbox2) # spazio tra riga corrente e successiva, se e' piu' piccolo di un tot riamngo nella stessa riga

			if  float(differenzaBbox) > 11 or float(differenzaBbox) < -3 or bordo == True :
				bordo = False

				stringa = [PDFrigaPerRiga ,precAltezza]
				PDFrigaPerRigaArray += [stringa]

				PDFrigaPerRiga = ""
				primaH = True
			else :
				if precLettera!="-":
					PDFrigaPerRiga = PDFrigaPerRiga +" "+lettera
				else:
					PDFrigaPerRiga = PDFrigaPerRiga +lettera

		precAltezza = altezza

		if string.find("<figure")>-1 : 			#se trovo <\figure> nel file xml mi segno la posizione della figura da cercare e la pagina nella quale cercare

			FigureDaCercare +=[altezza]
			FigureDaCercare +=[pagina]

		precBbox = Bbox2 

		
		if colonne < 131:       #!!!!!!!!!!!!!!!!!!!!!!!!! 2 COLONNE (ACM) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			Titolo = ricercaPDF.ricercaTitoloPDF2Colonne(fontStringa, dimensioneLettera, dimensioneTitolo,Times, Titolo, lettera, precLettera,diffSpazi)

			Capitolo, nStringa = ricercaPDF.ricercaCapitoloPDF2Colonne(Capitolo, nStringa , stringaNumero, lettera, precLettera, dimensioneLettera, dimensioneTitolo, fontStringa, Times, diffSpazi, Nimbus, Upper, CAPITOLI)
			
		else:				#!!!!!!!!!!!!!!!!! 1 COLONNA (LNCS) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

			if stringaNumero == 4:
				fontTitolo = fontStringa
				nStringa = stringaNumero -1

			Titolo, nStringa = ricercaPDF.ricercaTitoloPDF1Colonna(fontStringa, fontTitolo, dimensioneLettera, dimensioneTitolo, nStringa, stringaNumero, Times, Titolo, lettera, precLettera, diffSpazi)

			Capitolo, nStringa ,primo, fontCapitolo, dimensioneCapitolo = ricercaPDF.ricercaCapitoliPDF1Colonna(nStringa, stringaNumero, lettera, precLettera, Capitolo, Times, diffSpazi, primo, fontStringa, dimensioneCapitolo, dimensioneLettera, fontCapitolo, Nimbus, Upper, CAPITOLI )

		precSpazi = spazi2
		precLettera = lettera

		######## fine ciclo riga per riga del documento ########################

	documento.close()

	if len(Titolo)>1:
		while Titolo[0] == " ":
			Titolo = Titolo[1:]


	Titolo = inserisci_spazi.elimina_caratteri_speciali(Titolo)

	if colonne < 131:			# prendo solo i capitoli di primo livello

		tempCap = []
		for x in CAPITOLI:
			if len(x)>2:	
				if '0'<= x[0] <= '9' and not '0'<=x[2]<='9':
					tempCap+=[x]

		CAPITOLI = tempCap

	doc = doc.strip("outfile")
	doc = doc.replace(" ","")

	if len(CAPITOLI) == 0:
		CAPITOLI += ["1 Abstract"]

	stringa = [PDFrigaPerRiga ,precAltezza]
	PDFrigaPerRigaArray +=[stringa]
	paginePDF += [PDFrigaPerRigaArray]

	FIGURE = ricercaFigureTabelle.ricercaFigure(paginePDF, FigureDaCercare)

	TABELLE = ricercaFigureTabelle.ricercaTabelle(paginePDF, pagina)

	#CAPITOLI = creazione_risultati.creaFileRisultati(doc, Titolo , CAPITOLI, FIGURE, TABELLE, colonne) #se si decommenta crea un file di testo con i risultati (bisogna aggiungere la cartella in cui si vogliono mettere i risultati)
	
	g = creazione_grafo.creaGrafoRDF(doc, Titolo , CAPITOLI, FIGURE ,TABELLE )

	

	if graphOrRdf == "-graph":			# se e' stato scelto -graph faccio la post
		my_post.post(g, URLendpoint, graphURI)

	else :							#se e' stato scelto -rdf creo i file.rdf contenenti il grafo del documento
		DOCUMENTI += [doc]
		documento = open(directoryOutput+"/"+doc+"-grafo.rdf", "w")
		g = g.serialize(format="turtle")
		documento.write(g)
		documento.close()


if graphOrRdf == "-rdf":	#se e' stato scelto -rdf creo un file.rdf contenente il grafo di tutti i file presenti nella directory di input
	directoryInput = directoryInput.replace("/", "-")
	documento = open(directoryOutput+'/'+directoryInput+'.rdf', "w")
	for x in DOCUMENTI:
		docrdf = open(directoryOutput+'/'+x+'-grafo.rdf',"r")
		for y in docrdf:
			if primoDocumento:
				documento.write(y)
			else:
				if y.find("prefix") == -1:
					documento.write(y)

		primoDocumento = False


	docrdf.close()
	documento.close()

print "eseguzione avvenuta con successo" #### Fine Esecuzione