# TweetSense
An experiment with Tweeter Sentiment Analysis in Python 

Observaciones Importantes: 
* Para desarrollo se ha utilizado el lenguaje Python 3.6 de 64 bits. Son aún necesarias las siguientes librerías, que deben ser instaladas utilizando el comando “pip instal” 
    * Para análisis y generación de gráficos: 
        * pandas 
	    * numpy 
	    * plotly 
	* Para el análisis de sentimiento: 
        * subprocess 
        * shlex 
	* Para descarga de dados de tweeter 
        * tweepy 
        * matplotlib 

* Para ejecución los ficheros utilizan variables de ambiente definidas en las primeras líneas de código de cada módulo y estas deben ser ajustadas para correcto funcionamiento de la aplicación. 

* La aplicación “sentistrength.jar” utilizada para realizar el análisis de sentimiento, tiene licencia de uso restricta y no es distribuida junto a esta aplicación. Su uso académico es gratuito pero su uso comercial es pago. El código y librerías de distintos idiomas pueden ser obtenidos en por contacto directo el equipo de investigación responsable. Michael Thelwall (wlv.ac.uk) o David Vilares Calvo (udc.es) 
  
En la carpeta del proyecto se destacan las siguientes subcarpetas: 
* \InBox: Carpeta donde ficheros CSV deben ser colocados para análisis 
* \DoneBox: 	Carpeta 	donde 	ficheros 	CSV 	son 	movidos 	luego 	tras procesamiento 
* \DataStore: Carpeta donde ficheros de datos creados son almacenados 
* \Report: Carpeta donde ficheros html son almacenados para publicación. 
* \Sentistrength: Carpeta con la librería de análisis de sentimiento. 
 
En la tabla siguientes se presentan los módulos y una sugerencia de periodicidade para ejecución, caso programadas llamadas automáticas . 
 
Módulo | Función | Periodicidade
------------ | ------------- | ------------- 
TweetDownload.py | Hace la descarga de tweets conteniendo las palabra clave elegidas | Cada 15 minutos 
TweetLoad.py | Carga Tweets almacenados en formato CSV y realiza análisis de sentimiento, creando un fichero llamado “AllTweet.pkl” con todos los resultados Caso cargados nuevos ficheros, estos son añadidos al fichero plk original. | En seguida a cada TweeDownload.py o siempre que la carpeta \Inbox tenga su contenido alterado. 
Analyse.py | Carga el fichero “AllTweet.pkl” y realiza análisis de resumo, creando tablas almacenadas en ficheros específicos | En seguida a cada TweeLoad.py o siempre que el fichero AllTweet.plk sea modificado. 
Table.py | Carga las tablas producidas por Analyse.py y produce un informe en formato HTML para presentación en formato texto. | En seguida a cada Analyse.py o siempre que los ficheros plk sean alterados.
Graph.py | Carga las tablas producidas por Analyse.py y produce un informe en formato HTML para presentación en formato de gráficos. | En seguida a cada Analyse.py o siempre que los ficheros plk sean alterados. 
DASHBOARD.html | Carga páginas HTML creadas por Table.py y Graph.py en el formato de un cuadro de mando. | Actualizaciones automaticas generadas por Graph.py 
 
La aplicación genera los siguientes ficheros. 
1. AllTweet.pkl: Creado por “TweetLoad.py”, almacena todos los tweets en un fichero, sin duplicaciones y con informaciones adicionales de análisis de sentimiento. 
2.	TopPop.csv y TopPop.pkl: Tabla resumen con información de los usuarios más populares en función del número de seguidores. Indica la cantidad de tweets en un periodo de tiempo, asociados a una empresa (“label”). Totales y resumen de sentimiento 
3.	TopRetweet.csv y TopRetweet.pkl: Tabla resumen con información de los tweets que tuvieran más retweets. Indicada cantidad de retweets para periodo de tiempo y empresa (“label”). Incluye informaciones de sentimiento. 
4.	TopUser.csv y TopUser.pkl: Tabla resumen con información de los usuarios que publicaran más tweets. Indica la cantidad de tweets en un periodo de tiempo, asociados a una empresa (“label”). Totales y resumen de sentimiento 
5.	TweetCount.csv y TweetCount.pkl: Tabla resumen con información de la cantidad de tweets en un periodo de tiempo, asociados a una empresa (“label”). Totales y por sentimiento 
6.	TableReport.html: Tablas en formato HTML para publicación 
7.	emtvalencia_online.csv, metrovalencia_online.csv y valenbisi_online.csv: presentan los dados de twitter descargados por el modulo de Tweetdownload.py  
