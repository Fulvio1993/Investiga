Tool che restituisce, per ogni articolo indicato, un file in formato CSV contenente le informazioni indicate relative al articolo
PDF presente sul database RDF.

Per utilizzarlo bisogna utilizzare il seguente comando da terminale:

my get.py DirectoryInput Opzioni[capitoli |tabelle |figure |all] FileConfigurazione UrlEndpoint UriGrafo DirectoryOutput

dove:

• DirectoryInput: è la directory contenente gli articoli PDF dei quali si intende
estrarre le informazioni presenti nel database RDF.

• Opzioni: con questo parametro si indica quale tipo di informazione si vuole estrarre: 
se si indica capitoli si chiede di estrarre i nomi dei capitoli di primo livello, configure di estrarre le didascalie delle figure,
con tabelle di estrarre le didascalie delle tabelle. Inoltre si può anche utilizzare l’opzione all per indicare all’applicazione
di estrarre tutte le informazioni ( sia capitoli, sia didascalie figure, sia didascalie tabelle ).

• FileConfigurazione: il file di configurazione è un file di testo contenente il titolo
che si vuole assegnare, per ogni articolo PDF cercato nel database RDF, al file

• UrlEndpoint: è l’url del database sul quale si vuole eseguire la get.

• UriGrafo: è l’uri del grafo sul quale si vuole eseguire la get.

• DirectoryOutput: indirizzo della directory nella quale si vuole inserire i file restituiti dall’esecuzione di my get.py.
