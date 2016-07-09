Per funzionare investiga ha bisogno del pacchetto SPARQLWrapper e della libreria PDFMiner nella solita directory contenente 
i vari moduli di Investiga.

Per eseguire questo tool bisogna lanciare da terminale il comando:

main.py DirectoryInput DirectoryOutfileXML Opzioni[-graph | -rdf] [UrlEndpoint e UriGrafo | DirectoryOutput]

dove:
-DirectoryInput: Directory contenente gli articoli scientifici in formato PDF che si intendono processare.

DirectoryOutfileXML: Directory nella quale inserire i file XML prodotti. 

-graph: se s'intende eseguire la post del grafo ottenuto sull'UrlEndpoint e UriGrafo che andranno indicati di seguito, 
2 parametri separati.

-rdf: se s'intende creare un file.rdf contenente il grafo prodotto, indicando la Directory nella quale inserire qesto file.rdf.
