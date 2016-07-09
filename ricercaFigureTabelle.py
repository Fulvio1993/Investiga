#!/usr/bin/python2
import inserisci_spazi

def ricercaFigure( paginePDF, FigureDaCercare):
	
	i = 0
	FIGURE = []
	FigureTrovate = []
	
	while i< len(FigureDaCercare)-1:
		for x in paginePDF[FigureDaCercare[i+1]-1]: 	# cerco nella pagina in cui cercare

			# se trovo Fig o igure in un certo range
			if x[1] < FigureDaCercare[i]+30 and x[1] > FigureDaCercare[i]-107 and (x[0].find("Fig")>-1 or x[0].find("igure")>-1 or x[0].find("ig.")>-1): 

				if x[0].find("igure") >-1:
					pos = x[0].find("igure")

				elif x[0].find("Fig")>-1 :
					pos = x[0].find("Fig")
				
				else :
					pos = x[0].find("ig.")

				if pos <25 and len(x[0]) <440:	# se Figure o Fig e vicino all'inizio della stringa

					FigureTrovate +=[x[1]]
					
					if len(x[0])>3:		# tolgo quello che nn mi serve dalla stringa

						while x[0][len(x[0])-1] == " ":
							x[0] = x[0][:len(x[0])-1]

						if x[0].find("gure")>-1:
							pos =x[0].find("gure")
						if pos <5:
							x[0] = x[0][pos+6:]

						else:
							pos = x[0].find(":")
							x[0] = x[0][pos+1:]
					
						while not ('a'<=x[0][0]<='z' or 'A'<= x[0][0] <='Z') and len(x[0]) >1 and x[0][1]!="-":
							x[0] = x[0][1:]

						x[0] = inserisci_spazi.elimina_caratteri_speciali(x[0])

					FIGURE +=[x[0]]		# aggiungo la stringa alla struttura FIGURE 

					break

		i = i+2

	return FIGURE


def ricercaTabelle(paginePDF, pagina):

	TABELLE = []
	i = 0
	while i < pagina:

		for x in paginePDF[i]:		#per ogni stringa per ogni pagina

			if x[0].find("Table")>-1:  # se trovo Table nella stringa

				pos = x[0].find("Table")

				if pos <3:	# se Table e' a inizio stringa ed e' seguito da : o . o maiuscola
					if '0'<= x[0][pos+6] <='9' and (x[0][pos+7] ==":" or x[0][pos+7]=="." or(x[0][pos+7]==" " and 'A'<= x[0][pos+8]<='Z')):

						while x[0][len(x[0])-1] == " ":
							x[0] = x[0][:len(x[0])-1]

						if len(x[0]) >10 : # tolgo la parte che non mi serve dalla stringa

							if x[0].find("Table")>-1:
								pos = x[0].find("Table")
								x[0] = x[0][pos+5:]

							while not ('a'<=x[0][0]<='z' or 'A'<= x[0][0] <='Z'):
								x[0] = x[0][1:]

							x[0] = inserisci_spazi.elimina_caratteri_speciali(x[0])

							TABELLE +=[x[0]]		#aggiungo la stringa alla struttura TABELLE

		i = i+1

	return TABELLE