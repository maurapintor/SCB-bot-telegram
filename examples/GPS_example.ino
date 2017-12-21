#include <SoftwareSerial.h>

#include <TinyGPS.h>

/* This sample code demonstrates the normal use of a TinyGPS object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/

TinyGPS gps;
SoftwareSerial ss(4, 3);

static void smartdelay(unsigned long ms);
static String print_date(TinyGPS &gps);
bool flag = 0;

void setup()
{
  Serial.begin(115200);
  ss.begin(9600);
}

void loop()
{
  float flat, flon;
  unsigned long age, date, time, chars = 0;
  String data;
  if (flag){
    gps.f_get_position(&flat, &flon, &age);
    
    Serial.println(flat, 6);
    Serial.println(flon, 6);
    Serial.println(gps.f_speed_kmph(), 6);
    data = print_date(gps);
    Serial.println();
    smartdelay(5000);
  }
  else {
    gps.f_get_position(&flat, &flon, &age);
    smartdelay(5000);
    flag = 1;
  }
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
