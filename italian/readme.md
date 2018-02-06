# SCB - Smart Car Box

In questo readme è presentato il progetto SmartCarBox (SCB) realizzato dal pizza-team, un gruppo di studenti dell'Università di Cagliari. Il progetto fa seguito ai laboratori del Corso di Reti Radiomobili (Corso di Studi di Ing. delle Telecomunicazioni).

Contributori:
* Matteo Anedda (docente del corso)
* Enrico Ferrara
* Maurra Pintor
* Marco Uras


## Funzionalità richieste dal progetto

Sviluppare un sistema per il tracciamento di un veicolo tramite GPS. Il trigger per l'accensione del sistema è un accelerometro, che tramite un semplice algoritmo si accorge quando la macchina si sta spostando e invia tempestivamente un messaggio tramite Telegram al proprietario della macchina. Il sistema fa uso provvisoriamente di connettività WiFi, ma sarebbe opportuno integrare un modulo GSM per renderlo completamente autonomo.

Sullo smartphone:
* si deve ricevere un messaggio automatico (con BOT Telegram) nel momento in cui si passa dallo stato statico ad uno stato con una variazione sulla direzione x (o y) superiore a 15 metri (o comunque la minima distanza che identifichi uno spostamento superiore alla normale ricalibrazione della posizione dovuta all’incertezza del posizionamento GPS).
* in un generico percorso da un punto A a un punto B, al raggiungimento del punto B (assenza di variazione direzione x o y – macchina ferma per un periodo superiore ai 30 secondi), il BOT Telegram deve comunicare le coordinate GPS della posizione statica.
* le coordinate GPS dello SBC devono essere fornite anche su specifica richiesta al BOT Telegram indipendentemente dal verificarsi degli eventi menzionati in precedenza (es., alla stringa “posizione” il bot deve rispondere con le coordinate GPS, ad esempio “@39.2292043 9.109925” in modo tale che tramite browser si riconduca al posizionamento).
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
* nodePOST_GPS.ino :    post sul datastore delle coordinate lette, funzionamento analogo a "nodeAlarmGPS.ino"
* post_gps_mqtt.ino :   funzionamento analogo a "nodePOST_GPS.ino", con aggiunta di richiesta coords tramite mqtt

## Istruzioni

### Setup dell'Hardware

#### Boards

Nel sistema si è scelto di utilizzare un Arduino UNO per gestire il trigger con accelerometro, e un NodeMCU V3 per la connettività e lettura coordinate GPS. Le due board sono connesse tramite un piedino digitale.

| Connessioni                                     |
|:------------------------------------------------|
| D7 (GPIO13) NodeMCU --> 10K Ohm --> D2 Arduino  |
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

#### GPS

| Connessioni                                     |
|:------------------------------------------------|
| VCC GPS --> 5V Arduino                          |
| RX GPS --> D4 NodeMCU (GPIO2)                   |
| TX GPS --> D2 NodeMCU (GPIO4)                   |
| GND GPS --> GND                                 |

Il GPS ha anche bisogno di un'antenna. Per questo caso specifico si consiglia di usare una External Active Antenna come [questa](https://www.adafruit.com/product/960).

## Setup del software

#### WiFi e parametri da personalizzare


#### Cloud services


USIAMO SERVIZI CLOUD

#### Google cloud platform

Per l'hosting del bot e del database dobbiamo utilizzare servizi Cloud. Abbiamo scelto di usare [Google Cloud Platform](https://cloud.google.com) (GCP). Per proseguire nel tutorial è necessario avere un account Google (per crearne uno seguire questo [link](https://accounts.google.com/SignUp)).

Una volta effettuato l'accesso, è necessario creare un progetto su [GCP console](https://console.cloud.google.com). 

Creazione del progetto: 
![alt text](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/images/create_project.png "Create Project")

Creazione applicazione App Engine, semplicemente aprendo la shell di gcloud nel menu appengine:
![alt text](https://github.com/Maupin1991/SCB-bot-telegram/blob/master/images/app_engine.png "Create Project")

IMAGE


#### Bot Telegram


