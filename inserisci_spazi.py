#!/usr/bin/python2

def to_upper(string):
	    ## Converte la stringa in maiuscolo.
	    upper_case = ""
	    for character in string:
	        if 'a' <= character <= 'z':
	            location = ord(character) - ord('a')
	            new_ascii = location + ord('A')
	            character = chr(new_ascii)
	        upper_case = upper_case + character
	    return upper_case


def elimina_caratteri_speciali(string):

	string = string.replace('\x82', "fl")
	string = string.replace('\x81', "fi")
	string = string.replace('\x80', "ff")
	string = string.replace('\xb5', "ff")			
	string = string.replace('\x1b', 'ff')
	string = string.replace('\x9c', "'")
	string = string.replace('\x9d', "'")
	string = string.replace('\x15', " - ")
	string = string.replace('\xb7', "*")
	string = string.replace('\01', "e")
	string = string.replace('\xb8',"O")
	string = string.replace('\x98', "'")
	string = string.replace('\x99', "'")
	string = string.replace('\x92', ">")
	string = string.replace('\xb4', "d")
	string = string.replace('\x93', "-")
	string = string.replace('\x97', "x")
	string = string.replace('\x94', "-")						
	string = string.replace("  ", " ")

	return string


#in base al tipo di contesto (titolo, capitolo, figure e tabelle) e se la lettera e maiuscola o maiuscola o altro e allo spazio tra lettera precLettera inserisco gli spazi

def Titolo(Titolo, lettera, precLettera, diffSpazi): 

	if 'A'<=lettera<='Z' :	  # lettera maiuscola	
		if (float(diffSpazi) > 14 or float(diffSpazi)<0) and precLettera != "W" and precLettera !="M":
			Titolo = Titolo + " "

	else:					#lettera minuscola
		if (float(diffSpazi) > 11 or float(diffSpazi)<0) and precLettera!= "m" and precLettera !="w" and precLettera!= to_upper(precLettera):
			Titolo = Titolo + " "


	if lettera == to_upper(lettera) and precLettera != to_upper(precLettera) and lettera != ":" and lettera !="," and lettera!= "-":
		Titolo = Titolo + " "


	if 'a' <= lettera <= 'z' and precLettera == to_upper(precLettera):

		Titolo = Titolo[ : len(Titolo)-1]
		Titolo = Titolo +" " + precLettera

	Titolo = Titolo.replace("  ", " ")

	return Titolo



def Capitolo(Capitolo, lettera, precLettera, diffSpazi, Nimbus, Upper):

	if'A'<= lettera <= 'Z':			# lettera maiuscola e font diverso da Nimbus
		if Nimbus == False:
			if (float(diffSpazi) > 6 or float(diffSpazi)<0) and precLettera != "W" and precLettera !="M" and not(precLettera =="m" and float(diffSpazi)<10) and Upper ==False: #(FIX 3NER 1321 2)	
				Capitolo = Capitolo + " "

			elif Upper == True:				#serie di lettere maiuscole
				if(float(diffSpazi) >14 ):
					Capitolo = Capitolo +" "

		else:				#font Nimbus
			if (float(diffSpazi) > 10 or float(diffSpazi)<0) and precLettera != "W" and precLettera !="M" or(precLettera =="S" and float(diffSpazi)> 8):#and Upper(FIX 3NER 1321 2)	
				Capitolo = Capitolo + " "

	else:		#lettera minuscola
		if (float(diffSpazi)>7.5 or float(diffSpazi)<0) and 'a'<= precLettera<='z' and precLettera !='m' and precLettera !='w' and precLettera != "p" :
			Capitolo = Capitolo+" "
			
	if float(diffSpazi)> 6.9 and precLettera =='l':
		Capitolo = Capitolo +" "

	if precLettera == ":":
		Capitolo = Capitolo + " "

	Capitolo = Capitolo.replace("  ", " ")

	return Capitolo



def Figura(Figura, lettera, precLettera, diffSpazi):

	#precLettera minuscola
	if (float(diffSpazi)>5.9 or float(diffSpazi)<0) and 'a'<= precLettera<='z' and not (precLettera  =='m' and float(diffSpazi)<10) and not( precLettera =='w' and float(diffSpazi)<9) and not(precLettera == "p" and float(diffSpazi)<7) and precLettera != "b":
		Figura = Figura+" "

	# precLettera maiusola
	if (float(diffSpazi)>8.4 or float(diffSpazi)<0) and 'A'<= precLettera<='Z' and not (precLettera  =='M' and float(diffSpazi)<13) and not( precLettera =='W' and float(diffSpazi)<12) or precLettera =="I" and float(diffSpazi)>6.4:
		Figura = Figura+" "

	# inserisco spazi dopo , . ) : = in alcuni casi
	if (precLettera == "," or precLettera =="." or precLettera ==")" or precLettera ==":" or precLettera =="=")and lettera !="." and not '0'<= lettera <='9':
		Figura = Figura +" "

	# alcune lettere occupano uno spazio minore e quindi inserisco lo spazio anche se diffSpazi se piu' piccolo
	if (precLettera =="t" or precLettera =="l" or precLettera =="s"  or precLettera =="f" ) and float(diffSpazi) >4.4 :
		Figura = Figura +" "

	if( precLettera == "r" and lettera!="m") and float(diffSpazi)>5.2 :
		Figura = Figura + " "

	# controllo quando inserire gli spazi dopo i numeri
	if ('0'<=precLettera <='9' or ('0'<=lettera<='9' and precLettera !="@")) and float(diffSpazi)> 6.7:	
		Figura = Figura +" "

	# controllo quando inserire gli spazi dopo } e *
	if (precLettera =="}" or precLettera == "*") and ('a'<= lettera <='z' or 'A'<= lettera <='Z'):
		Figura = Figura +" "

	Figura = Figura.replace("  ", " " )
	return Figura