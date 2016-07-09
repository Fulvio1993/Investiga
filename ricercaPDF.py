#!/usr/bin/python2
import inserisci_spazi

#################################################### 2 COLONNE (ACM) ###################################################

def ricercaTitoloPDF2Colonne(fontStringa, dimensioneLettera, dimensioneTitolo, Times, Titolo ,lettera, precLettera, diffSpazi):
	# se il font e' Bold e la dimensione e' quella dle titolo allora aggiungo la lettera al titolo
	if fontStringa.find("Bold") > -1  and  round(float(dimensioneLettera)) == round(float(dimensioneTitolo)):
		if Times ==False:
			Titolo = inserisci_spazi.Titolo(Titolo, lettera, precLettera, diffSpazi)

		Titolo = Titolo + lettera

	return Titolo


def ricercaCapitoloPDF2Colonne(Capitolo, nStringa, stringaNumero, lettera, precLettera, dimensioneLettera, dimensioneTitolo, fontStringa, Times, diffSpazi, Nimbus, Upper, CAPITOLI):
	
	# se il capitolo e' finito l'aggiungo alla struttura CAPITOLi
	if (nStringa+1 != stringaNumero) or ('0' <= lettera <='9' and (precLettera != "." )):
		if Capitolo:
			if len(Capitolo)>2:
				while Capitolo[0]== " ":
					Capitolo = Capitolo[ 1: ]
				while Capitolo[len(Capitolo)-1] ==" ":
					Capitolo = Capitolo[:len(Capitolo)-1]

				pos = Capitolo.find("  ")
				if pos > -1:
					temp = Capitolo[pos +1 :]
					Capitolo = Capitolo[:pos] + temp

				Capitolo = inserisci_spazi.elimina_caratteri_speciali(Capitolo)
				CAPITOLI += [Capitolo]
			Capitolo = ""
			
	# se il font e' Bold o Medi e la dimensione della lettera e maggiore di un tot aggiungo la lettera al capitolo
	if dimensioneLettera: 
		if (fontStringa.find("Bold") > -1 or fontStringa.find("Medi") >-1 or fontStringa.find("X12") >-1 or fontStringa.find("unknown")>-1) and round(float(dimensioneLettera)) < round(float(dimensioneTitolo)) and float(dimensioneLettera) > 10.0:
			nStringa = stringaNumero

			if Times == False:
				Capitolo = inserisci_spazi.Capitolo(Capitolo ,lettera, precLettera, diffSpazi, Nimbus, Upper)
				
			Capitolo = Capitolo + lettera	

	return Capitolo	,nStringa


################################################ 1 COLONNA (LNCS) ####################################################

def ricercaTitoloPDF1Colonna(fontStringa, fontTitolo, dimensioneLettera, dimensioneTitolo, nStringa, stringaNumero, Times, Titolo, lettera, precLettera, diffSpazi):

	# se il font e' quello del titolo e la dimensione e' quella del titolo aggiungo la lettera al titolo
	if (fontStringa == fontTitolo and dimensioneLettera == dimensioneTitolo and nStringa+1 == stringaNumero ): 
		nStringa = stringaNumero

		if Times == False:					# Devo inserire gli spazi 
			Titolo = inserisci_spazi.Titolo(Titolo, lettera, precLettera, diffSpazi)

		Titolo = Titolo + lettera

	return Titolo, nStringa


def ricercaCapitoliPDF1Colonna(nStringa, stringaNumero, lettera, precLettera, Capitolo, Times, diffSpazi, primo, fontStringa, dimensioneCapitolo, dimensioneLettera, fontCapitolo, Nimbus, Upper, CAPITOLI ):

	# solo capitoli principali (di primo livello)
	if (nStringa+1 != stringaNumero) or ('0' <= lettera <='9' and (precLettera != "." and precLettera!= " ")):

		if Capitolo:		# se il capitolo e' finito l'aggiungo alla struttura CAPITOLI
			if len(Capitolo)>3:
				pos = Capitolo.find("  ")
				if pos > -1:
					temp = Capitolo[pos +1 :]
					Capitolo = Capitolo[:pos] + temp

				Capitolo = inserisci_spazi.elimina_caratteri_speciali(Capitolo)
				CAPITOLI += [Capitolo]

			Capitolo = ""

	if Times == True:								
		if fontStringa.find("Bold")> -1:	# se il font e' Bold e trovo 1 mi salvo la dimensione capitolo
			if precLettera == ' ' and lettera == "1" and primo == True:		
				dimensioneCapitolo = float(dimensioneLettera)
				primo = False

			if float(dimensioneLettera) == float(dimensioneCapitolo):	#se la dimensione e' quella del capitolo aggiungo la lettera al capitolo
				Capitolo = Capitolo + lettera
				nStringa  = stringaNumero

	else: # se i capitoli non sono in Bold mi salvo font e dimensione dei capitoli quando trovo '1I' (1INTRODUCTION)
		if precLettera== '1' and lettera == 'I' and primo == True:
			lettera = "1"+lettera
			fontCapitolo = fontStringa
			dimensioneCapitolo = float(dimensioneLettera)
			if Capitolo.find("Introduction")>-1:
				primo = False
		
		# se la lettera ha un certo font e una certa dimensione l'aggiungo al capitolo
		if (fontStringa.find("Medi") > 0 or fontStringa.find("12")> 0 or fontStringa.find("Bold") >0 or fontStringa.find("unknown")>-1 ) and (float(dimensioneLettera) == float(dimensioneCapitolo)):
			
			nStringa = stringaNumero

			Capitolo = inserisci_spazi.Capitolo(Capitolo, lettera, precLettera, diffSpazi, Nimbus, Upper)

			Capitolo = Capitolo + lettera

			if primo:
				lettera = lettera[1 : ]
				primo = False

	return Capitolo, nStringa, primo, fontCapitolo, dimensioneCapitolo