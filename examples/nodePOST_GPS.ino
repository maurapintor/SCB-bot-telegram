

#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
//---------------------------------------------------------------------------------//

/*
 * Wi-Fi settings
 */

char ssid[]     = "we<3pizza";    // your network SSID (name)
char password[] = "pizzateam";    // sqwswzxaqyour network key
//---------------------------------------------------------------------------------//


/*
 *     GPS settings
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
 * Pin settings
 */
int alarmPin = 13;
int active = LOW;
int ledPin = LED_BUILTIN;
//---------------------------------------------------------------------------------//

String apiKey ="ZMJLQ6404L2F2RWE";
const char* server = "api.thingspeak.com";
int sent = 0;


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
}

void loop() {

active = digitalRead(alarmPin);
Serial.println(active);
if(active == HIGH){
  printPosition();
  }
delay(10);

}


//---------------------------------------------------------------------------------//


/*
 * GPS Functions
 */
void printPosition(){
  if (flag){
    gps.f_get_position(&flat, &flon, &age);
    
    Serial.println(flat, 6);
    Serial.println(flon, 6);
    Serial.println(gps.f_speed_kmph(), 6);
    data = print_date(gps);
    Serial.println();
    smartdelay(1000);
   }
  else {
    gps.f_get_position(&flat, &flon, &age);
    smartdelay(1000);
    flag = 1;
  }
}


void sendPosition(float lat, float lon)
{  
   WiFiClient client;
  
   if (client.connect(server, 80)) { // use ip 184.106.153.149 or api.thingspeak.com
   Serial.println("WiFi Client connected, sending data ");
   
   String postStr = apiKey;
   postStr += "&field1=";
   postStr += String(lat);
   postStr += "&field2=";
   postStr += String(lon);

   postStr += "\r\n\r\n";
   String coords = String(lat, 6) + "," + String(lon, 6);

   
   client.print("POST /update HTTP/1.1\n");
   client.print("Host: api.thingspeak.com\n");
   client.print("Connection: close\n");
   client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
   client.print("Content-Type: application/x-www-form-urlencoded\n");
   client.print("Content-Length: ");
   client.print(postStr.length());
   client.print("\n\n");
   client.print(postStr);
   delay(1000);
   
   }//end if
   sent++;
 client.stop();
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
    
    sprintf(sz, "%02d/%02d/%02d %02d:%02d:%02d ",
        month, day, year, hour, minute, second);
    Serial.print(sz);
  }
  smartdelay(0);
  data = String(sz);
  return data;
}

