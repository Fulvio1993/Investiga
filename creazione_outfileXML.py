#!/usr/bin/python2

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import XMLConverter

import sys


def trasformaPDFinXML(doc, directoryOutfile):			# PDF Miner solo parte che mi serve (trasforma PDF in XML)

	password = ""
	pagenos = []
	i = 0
	codec ="utf-8"
	laparams = None 
	imagewriter = None 
 
	doc = doc.replace(" ","")
	fp = open(doc, 'rb')	

	doc = doc.replace("/", "_")
	pos = doc.find(".pdf")
	doc = doc[: pos]
	doc ="outfile "+ doc

	# Create a PDF parser object associated with the file object.
	parser = PDFParser(fp)
	# Create a PDF document object that stores the document structure.
	# Supply the password for initialization.
	document = PDFDocument(parser, password)
	# Check if the document allows text extraction. If not, abort.
	if not document.is_extractable:
	    raise PDFTextExtractionNotAllowed
	# Create a PDF resource manager object that stores shared resources.
	rsrcmgr = PDFResourceManager()
	outfp = file(directoryOutfile+"/"+doc,"w") 

	device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, imagewriter=imagewriter)

	# Create a PDF interpreter object.
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	# Process each page contained in the document.
	for page in PDFPage.create_pages(document):
	    interpreter.process_page(page)
	  
	fp.close()
	device.close()
	outfp.close()

	return doc