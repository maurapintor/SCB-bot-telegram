# SCB - Smart Car Box

In questo readme è presentato il progetto SmartCarBox (SCB) realizzato dal pizza-team, un gruppo di studenti dell'Università di Cagliari. Il progetto fa seguito ai laboratori del Corso di Reti Radiomobili (Corso di Studi di Ing. delle Telecomunicazioni).

Contributori:
* Matteo Anedda (docente del corso)
* Enrico Ferrara
* Maurra Pintor
* Marco Uras

Nota: se vuoi saltare l'introduzione e sai già come funziona il sistema, clicca [qui](#istruzioni).


## Funzionalità richieste dal progetto

Sviluppare un sistema per il tracciamento di un veicolo tramite GPS. Il trigger per l'accensione del sistema è un accelerometro, che tramite un semplice algoritmo si accorge quando la macchina si sta spostando e invia tempestivamente un messaggio tramite Telegram al proprietario della macchina. Il sistema fa uso provvisoriamente di connettività WiFi, ma sarebbe opportuno integrare un modulo GSM per renderlo completamente autonomo.

Sullo smartphone:
* si deve ricevere un messaggio automatico (con BOT Telegram) nel momento in cui si passa dallo stato statico ad uno stato con una variazione sulla direzione x (o y) superiore a 15 metri (o comunque la minima distanza che identifichi uno spostamento superiore alla normale ricalibrazione della posizione dovuta all’incertezza del posizionamento GPS).
* in un generico percorso da un punto A a un punto B, al raggiungimento del punto B (assenza di variazione direzione x o y – macchina ferma per un periodo superiore ai 30 secondi), il BOT Telegram deve comunicare le coordinate GPS della posizione statica.
* le coordinate GPS dello SBC devono essere fornite anche su specifica richiesta al BOT Telegram indipendentemente dal verificarsi degli eventi menzionati in precedenza (es., alla stringa “posizione” il bot deve rispondere con le coordinate GPS, ad esempio “\@39.2292043 9.109925” in modo tale che tramite browser si riconduca al posizionamento).
* Il tracking e la posizione devono essere visualizzati su mappa attraverso una
applicazione in ambiente Android

## Aggiunte proposte dal team

Il team ha apportato le seguenti modifiche al funzionamento:

* le coordinate sono inviate tramite Telegram con una visualizzazione della mappa, non più come sola stringa testuale
* il bot di telegram è stato caricato su Google App Engine per consentire funzionalità più complesse, come l'invio della location su mappa o la risposta ai messaggi anche quando il modulo non è connesso


## Materiale a disposizione

* Due antenne GPS – External Active Antenna
* Due cavi adattatori con connettore UFL-SMA
* Una antenna GPS con modulo Ublox NEO6MV2 GY-GPS6MV2
* Resistenze necessarie al modulo Ublox NEO6MV2 GY-GPS6MV2
* 1 ESP8266 NODE MCU V3
* 1 cavetto micro usb
* 1 cavetto per Arduino
* 1 Arduino UNO
* 1 modulo accelerometro (xyz) MMA7361 (analogico)
* Cavetteria/dupont necessari: 20 M-M + 10 M-M + 10 M-M + 2 F-F
* Breadboard
* 1 kit: 3 led, 5+5+1+1 resistenze, 1 diodo, 1 fotoresistore, 3 pulsanti
* Alimentatore esterno per ESP 5V
* Alimentatore esterno via USB 5V
* Power bank

## Contenuto del repository

* examples :    sketch di esempio per test dei singoli moduli
* handlers :    funzionalità del bot telegram e gestione dati
* images :      immagini per il tutorial
* italian :     cartella del readme in italiano
* models :      gestione datastore (tabelle)
* templates :   visualizzazione della mappa
* utils :       classi di utilità
* README.md :   readme del repository (inglese)
* app.yaml :    configurazione Google App Engine
* main.py :     main file GAE

## Lista degli sketch esempio

* GPS_example.ino :     lettura dati GPS e stampa su seriale
* acc_gps.ino :         stampa coordinate GPS quando è rilevato un movimento (tramite accelerometro) - solo Arduino
* motion_detector.ino : sensore di movimento tramite lettura accelerometro (accensione del led come "allarme")
* nodeAlarmGPS.ino :    stampa coordinate GPS su nodeMCU quando è rilevato un movimento (tramite accelerometro) su Arduino
* nodePOST_GPS.ino :    post su [ThingSpeak](www.thingspeak.com) delle coordinate lette, funzionamento analogo a                                       "nodeAlarmGPS.ino"
* post_gps_mqtt.ino :   funzionamento analogo a "nodePOST_GPS.ino", con aggiunta di richiesta coords tramite mqtt e post su                           Google Datastore

## Istruzioni

### Setup dell'Hardware

Nella seguente sezione sono illustrati i passaggi per il montaggio fisico del sistema. Le connessioni effettuate sono illustrate nello schema seguente. Si consiglia di prenderne visione ed effettuare le connessioni nell'ordine di spiegazione del tutorial.

![Schematics](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/1.png)

#### Boards

Nel sistema si è scelto di utilizzare un Arduino UNO per gestire il trigger con accelerometro, e un NodeMCU V3 per la connettività e lettura coordinate GPS. Le due board sono connesse tramite un piedino digitale.

| Connessioni                                     |
|:------------------------------------------------|
| D7 (GPIO13) NodeMCU --> 10K Ohm --> D4 Arduino  |
| 3.3V Arduino --> breadboard +                   |
| GND Arduino --> breadboard -                    |

Le ultime due connessioni sono consigliate per la gestione dei cavi. In seguito il + e - della breadboard saranno chiamati 3.3V e GND.

#### Accelerometro

| Connessioni                                     |
|:------------------------------------------------|
| Z accelerometro --> A3 Arduino                  |
| Y accelerometro --> A4 Arduino                  |
| X accelerometro --> A5 Arduino                  |
| SL accelerometro --> 3.3V                       |
| 3V3 accelerometro --> 3V3                       |
| GND accelerometro --> GND                       |
| gSEL accelerometro --> GND                      |

Aggiungiamo la connessione di un led per verificare l'attivazione del trigger:

| Connessioni                                     |
|:------------------------------------------------|
| D2 Arduino --> resistenza 1k Ohm --> led --> GND|

#### GPS

| Connessioni                                     |
|:------------------------------------------------|
| VCC GPS --> 5V Arduino                          |
| RX GPS --> D4 NodeMCU (GPIO2)                   |
| TX GPS --> D2 NodeMCU (GPIO4)                   |
| GND GPS --> GND                                 |

Il GPS ha anche bisogno di un'antenna. Per questo caso specifico si consiglia di usare una External Active Antenna come [questa](https://www.adafruit.com/product/960).

## Setup del software

Andiamo a preparare gli script necessari su Arduino e NodeMCU (contenuti nella cartella "flash_to_boards"):

| Board  | Script                         |
|:-------|:-------------------------------|
| NodeMCU| flash_to_boards/SCBNode.ino    |
| Arduino| flash_to_boards/SCBArduino.ino |

Prima di caricare gli sketch sulla board è importante inserire alcuni parametri per il setup della connettività WiFi e le chiavi per le API.

### WiFi e parametri da personalizzare

Inserire nello script del NodeMCU i seguenti parametri. Fare attenzione alle lettere maiuscole e minuscole, o lo sketch non funzionerà correttamente.

```arduino
char ssid[]     = "";               // SSID della rete
char password[] = "";               // password
String yourProjectName = "";        // your GAE project name
```

#### Google cloud platform

Per l'hosting del bot e del database dobbiamo utilizzare servizi Cloud. Abbiamo scelto di usare [Google Cloud Platform](https://cloud.google.com) (GCP). Per proseguire nel tutorial è necessario avere un account Google (per crearne uno seguire questo [link](https://accounts.google.com/SignUp)).

Una volta effettuato l'accesso, è necessario creare un progetto su [GCP console](https://console.cloud.google.com). 

Creazione del progetto: 
![Creazione progetto](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/images/create_project.png "Create Project")

Creazione applicazione App Engine, semplicemente aprendo la shell di gcloud nel menu appengine:
![Creazione applicazione](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/images/app_engine.png "Create Project")

Annotare l'ID del progetto (Attenzione: potrebbe essere diverso dal nome perché gli ID sono univoci).

Completati i passaggi su GCP, si passa ora a configurare il progetto del bot telegram. Sarà necessario scaricare questo repository e modificare alcuni file di configurazione.

Il primo passo è quello di installare il software development kit (sdk) per Google App Engine e Python. Qui si trova il [tutorial](https://cloud.google.com/appengine/docs/standard/python/download) con i link utili e le istruzioni.

Bisognerà poi inserire il nome del progetto appena creato nel file presente nel repository:

|File            |
|----------------|
|app.yaml        |

```yaml
application: project-name
```



Seguire poi [questo tutorial](https://cloud.google.com/appengine/docs/standard/python/getting-started/deploying-the-application) per effettuare il deploy dell'applicazione.

#### Bot Telegram

Adesso è il momento di creare un nuovo bot con BotFather. Alla fine di questo processo avremo la chiave API necessaria per comandare il bot.

Per prima cosa cerchiamo \@BotFather su Telegram. Apriamo la conversazione e premiamo sulla scritta "avvia" o "start" in basso. Seguire le istruzioni per creare un nuovo bot.

[Tutorial Bot Father](http://www.nigiara.it/telegram/come-aprire-i-bot-su-telegram.htm)

I passaggi principali sono:

1. Cercare il profilo \@BotFather e avviare la conversazione
2. Inviare il comando /newbot
3. Inserire il nome per il bot
4. Inserire username per il bot (facendolo finire con la parola chiave "bot")
5. Prendere la API key che ci scrive BotFather

Ricordiamoci la API key, in quanto dovremo usarla in seguito.

Una volta effettuati i passaggi elencati, si può modificare il file:

|File            |
|----------------|
|utils/token.py  |

inserendo il token che ci ha dato BotFather.




## Richiesta posizione real-time

Per la richiesta di posizione in real-time, è necessario comunicare in maniera diretta con il dispositivo hardware.
Purtroppo non avendo a disposizione un indirizzo IP fisso e pubblico, non è possibile raggiungere il dispositivo con una normale chiamata HTTP, parimenti ad una pagina web.

Per questa funzionalità si può usare il protocollo [MQTT](http://www.lucadentella.it/2016/10/24/mqtt-introduzione/), è necessario però configurare sia il software su NodeMcu che sul web server.

**ATTENZIONE**: per proseguire è necessario utilizzare un bridge HTTP-MQTT in quanto il servizio cloud che abbiamo scelto non consente di farlo gratuitamente.
Nel seguito faremo riferimento ad un bridge gratuito e messo a disposizione dall'Università di Cagliari.
Inoltre sarà necessario utilizzare un proprio topic in modo tale che solo i nostri dispositivi lo ascoltino. 

Aprire il file *flash_to_boards/SCBNode.ino* e inserire l'indirizzo del bridge e il topic in corrispondenza delle righe:

|File                         |
|-----------------------------|
|flash_to_boards/SCBNode.ino  |

```arduino
const char* mqtt_server = "tools.lysis-iot.com";
String topic = "scb";
```

quindi quello che abbiamo utilizzato è:
*tools.lysis-iot.com*

Annotare il nome del topic perchè sarà utile nel seguito.

A questo punto abbiamo configurato il dispositivo in modo tale da farlo rimanere in ascolto sul nostro topic.

La seconda parte riguarda la configurazione del web server, colui che effettivamente utilizzerà la parte di bridge. Ricordiamo che il bridge si occupa di tradurre una chiamata HTTP in una publish/subscribe MQTT.

Ciò che dobbiamo fare è aprire il file *handlers/PositionRequestHandler.py* e modificare l'url e topic. L'url presente è relativo al servizio messo a disposizione dal dipartimento, se viene usato un altro bridge sarà necessario aggiornarlo.

Il topic deve essere modificato in ogni caso, inserendo quello scelto al passaggio precedente.

|File                                |
|------------------------------------|
|handlers/PositionRequestHandler.py  |

```python
url = 'http://tools.lysis-iot.com/MqttPublish/publish.php'
topic = 'scb'
```

Abbiamo configurato il web server in modo tale da fare una chiamata HTTP verso un servizio esterno, il quale si occupa di pubblicare sul topic MQTT desiderato. 

## Bonus material

Risultati ottenuti:
![Result](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/1b.jpg)
![Design](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/2.jpg)
![Work in progress](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/2b.jpg)
![Lots of code](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/3.jpg)
![Pizza team](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/assets/img/about/3b.jpg)
[smartcar-box.appspot.com](smartcar-box.appspot.com)











