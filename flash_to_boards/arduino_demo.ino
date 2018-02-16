

#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

/*
                     ----Made by Pizza-Team----
       This sketch detects movement through an accelerometer connected to Arduino
       and sends to serial monitor of NodeMCU the GPS coordinates when triggered
       (communication through alarmPin). Then it sends the values to the google datastore.
       IMPORTANT: set the connection variables before upload!
*/

//---------------------------------------------------------------------------------//

/*
   Connection settings
*/

char ssid[]     = "we<3pizza";    // your network SSID (name)
char password[] = "pizzateam";    // sqwswzxaqyour network key
String yourProjectName = "smartcar-box";
const char* mqtt_server = "tools.lysis-iot.com";
const char* topic = "scb";

//---------------------------------------------------------------------------------//


/*
       GPS settings
*/
TinyGPS gps;
SoftwareSerial ss(4, 2);

static void smartdelay(unsigned long ms);
static String print_date(TinyGPS &gps);
bool flag = 0;

float flat, flon;
unsigned long age, date, tempo, chars = 0;
String data;

//---------------------------------------------------------------------------------//

/*
   mqtt settings
*/
WiFiClient espClient;
PubSubClient mqttclient(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


/*
   Pin settings
*/
int alarmPin = 13;
int active = LOW;
int ledPin = LED_BUILTIN;
//---------------------------------------------------------------------------------//


String apiKey = "prova";
const char * host = ".appspot.com";
String server_name = yourProjectName + host;
const char *server = server_name.c_str();



int sent = 0;
unsigned long last_req = 0;
int sent_stop = 1;


void setup() {
  //Monitor output
  Serial.begin(38400);
  pinMode(alarmPin, INPUT);

  //GPS output
  ss.begin(9600);

  //Wi-fi output
  Serial.print("Connecting Wifi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  delay(500);
  pinMode(ledPin, OUTPUT);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    digitalWrite(ledPin, !digitalRead(ledPin));     // set pin to the opposite state
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);
  digitalWrite(ledPin, HIGH);

  mqttclient.setServer(mqtt_server, 1883);
  mqttclient.setCallback(callback);
}

void loop() {

  active = digitalRead(alarmPin);
  if (active == HIGH) {
    printPosition(false);
    last_req = millis();
    sent_stop = 0;
  }
  else{
  if (millis()-last_req > 180000 && !sent_stop){
    sendStop();
    sent_stop = 1;
  }
  }
  Serial.println(millis());
//  delay(10);
//  if (!mqttclient.connected()) {
//    reconnect();
//  }
//  mqttclient.loop();
//  delay(10);

}


//---------------------------------------------------------------------------------//


/*
   GPS Functions
*/
void printPosition(bool is_requested) {
  if (flag) {
    gps.f_get_position(&flat, &flon, &age);
    float fspeed = gps.f_speed_kmph();

    Serial.println(flat, 6);
    Serial.println(flon, 6);
    Serial.println(fspeed, 6);
    data = print_date(gps);
    Serial.println();
    sendPosition(flat, flon, fspeed, data, is_requested);
    smartdelay(1000);
  }
  else {
    gps.f_get_position(&flat, &flon, &age);
    smartdelay(1000);
    flag = 1;
  }
}


void sendPosition(float lat, float lon, float fspeed, String(data), bool is_requested)
{
  WiFiClient wificlient;

  if (wificlient.connect(server, 80)) {
    Serial.println("WiFi Client connected, sending data ");

    String postStr = "latitude=";
    postStr += String(lat, 6);
    postStr += "&longitude=";
    postStr += String(lon, 6);
    postStr += "&speed=";
    postStr += String(fspeed, 6);
    postStr += "&data=";
    postStr += data;
    postStr += "&apiKey=";
    postStr += apiKey;
    postStr += "&requested=";
    postStr += String(is_requested);
    Serial.println(is_requested);
    Serial.println(String(is_requested));

    postStr += "\r\n\r\n";
    String coords = String(lat, 6) + "," + String(lon, 6);

    wificlient.print("POST /position/put HTTP/1.1\n");
    wificlient.print("Host: "+yourProjectName+".appspot.com\n");
    wificlient.print("Connection: close\n");
    wificlient.print("Content-Type: application/x-www-form-urlencoded\n");
    wificlient.print("Content-Length: ");
    //   wificlient.print("apiKey: " + apiKey + "\n");

    wificlient.print(postStr.length());
    wificlient.print("\n\n");
    wificlient.print(postStr);
    delay(1000);


    while (wificlient.available()) {
      String line = wificlient.readStringUntil('\r');
      Serial.print(line);
    }
    Serial.println();
    Serial.println("closing connection");

  }//end if


  sent++;
  wificlient.stop();
  delay(5000);

}

static void smartdelay(unsigned long ms)
{
  unsigned long start = millis();
  do
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}

static String print_date(TinyGPS &gps)
{
  int year;
  byte month, day, hour, minute, second, hundredths;
  unsigned long age;
  String data;
  char sz[32];
  gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &age);
  if (age == TinyGPS::GPS_INVALID_AGE)
    Serial.print("********** ******** ");
  else
  {

    //sprintf(sz, "%02d/%02d/%02d %02d:%02d:%02d ",
    //    month, day, year, hour, minute, second);
    sprintf(sz, "%02d-%02d-%02d_%02d:%02d:%02d", month, day, year, hour, minute, second);
    Serial.print(sz);
  }
  smartdelay(0);
  data = String(sz);
  return data;
}

/*
   mqtt functions
*/

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  printPosition(true);

}


void reconnect() {
  // Loop until we're reconnected
  while (!mqttclient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (mqttclient.connect(clientId.c_str())) {
      Serial.println("connected");
      mqttclient.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttclient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}



void sendStop()
{
  WiFiClient wificlient;

  if (wificlient.connect(server, 80)) {
    Serial.println("WiFi Client connected, sending data ");

    String postStr = "apiKey=";
    postStr += apiKey;
    postStr += "&latitude=";
    postStr += flat;
    postStr += "&longitude=";
    postStr += flon;

    postStr += "\r\n\r\n";

    wificlient.print("POST /position/stop HTTP/1.1\n");
    wificlient.print("Host: "+yourProjectName+".appspot.com\n");
    wificlient.print("Connection: close\n");
    wificlient.print("Content-Type: application/x-www-form-urlencoded\n");
    wificlient.print("Content-Length: ");

    wificlient.print(postStr.length());
    wificlient.print("\n\n");
    wificlient.print(postStr);
    delay(1000);
  }

  }

