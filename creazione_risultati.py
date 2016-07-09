#!/usr/bin/python2

def creaFileRisultati(doc, Titolo, CAPITOLI, FIGURE, TABELLE, colonne):

	doc = doc.strip("outfile")
	documento = open("risultati/titolo e capitoli "  +doc, "w")

	documento.write("DOCUMENTO: " + doc)
	documento.write('\n')
	documento.write('\n')
	documento.write('\n')

	documento.write ("TITOLO:")
	documento.write('\n')
	documento.write('\n')

	documento.write (Titolo)							# problema 1518 8 carattere codifica
	documento.write('\n')
	documento.write('\n')
	documento.write('\n')

	documento.write("CAPITOLI DI PRIMO LIVELLO:")
	documento.write('\n')
	documento.write('\n')

	if colonne < 131:

		tempCap = []
		for x in CAPITOLI:	

			if '0'<= x[0] <= '9' and not '0'<=x[2]<='9':
				documento.write (x)
				documento.write ('\n')
				tempCap+=[x]

		CAPITOLI = tempCap


	else :
		for x in CAPITOLI:
			documento.write(x)
			documento.write('\n')

	documento.write('\n')
	documento.write('\n')
	documento.write("FIGURE:")
	documento.write('\n')
	documento.write('\n')

	for x in FIGURE:
		documento.write(x)
		documento.write('\n')
		documento.write('\n')

	documento.write('\n')
	documento.write('\n')
	documento.write('TABELLE:')
	documento.write('\n')
	documento.write('\n')

	for x in TABELLE:
		documento.write(x)
		documento.write('\n')
		documento.write('\n')



	documento.close()

	return CAPITOLI