

/*
 *                   ----Made by Pizza-Team----
 *     This sketch detects movement through an accelerometer
 *     and blinks the led when triggered
 */

/*
MMA7361 ACCELEROMETER:
  X --> A5
  Y --> A4
  Z --> A3
  3V --> 3.3V
  GND --> GND
  G-SEL --> GND
  SLEEP --> 3.3
  AREF ARDUINO --> 3.3V ARDUINO (THIS IS IMPORTANT FOR CALIBRATION)
*/


//Global Variables and constants
int buttonPin = HIGH; // button Pin connected to Analog 0


//Accelerometer Pins
const int x = A3; // X pin connected to Analog 3
const int y = A4; // Y pin connected to Analog 4
const int z = A5; // Z pin connected to Analog 5


//Alarm LED
const int ledPin = 2; // LED connected to Digital 2

int tolerance=150; // Sensitivity of the Alarm
boolean calibrated=false; // When accelerometer is calibrated - changes to true 
boolean moveDetected=false; // When motion is detected - changes to true



//Accelerometer limits
int xMin; //Minimum x Value
int xMax; //Maximum x Value
int xVal; //Current x Value

int yMin; //Minimum y Value
int yMax; //Maximum y Value
int yVal; //Current y Value

int zMin; //Minimum z Value
int zMax; //Maximum z Value
int zVal; //Current z Value



void setup(){
 //Begin Serial communication
 Serial.begin(38400);
 
 //Initilise LED Pin
 pinMode(ledPin, OUTPUT);
 
}



void loop(){
 // If the button is pressed, initialise and recalibrate the Accelerometer limits.
 if(buttonPin == HIGH){
 calibrateAccel();
 buttonPin = LOW;
 }
 
 // Once the accelerometer is calibrated - check for movement 
 
 if(checkMotion()){
 moveDetected=true;
 }
 
 // If motion is detected - sound the alarm !
 if(moveDetected){
 Serial.println("ALARM");
 ALARM();
 delay(100);
 moveDetected = false;
 }
 
}


//This is the function used to sound the buzzer
void buzz(int reps, int rate){
 for(int i=0; i<reps; i++){
 delay(100);
 delay(rate);
 }
} 




// Function used to calibrate the Accelerometer
void calibrateAccel(){
 // reset alarm
 moveDetected=false;
 
 //initialise x,y,z variables
 xVal = analogRead(x);
 xMin = xVal;
 xMax = xVal;
 
 yVal = analogRead(y);
 yMin = yVal;
 yMax = yVal;
 
 zVal = analogRead(z);
 zMin = zVal;
 zMax = zVal;
 
 // Calibration sequence initialisation sound - 3 seconds before calibration begins
 buzz(3,1000);
 
 //calibrate the Accelerometer (should take about 0.5 seconds)
 for (int i=0; i<50; i++){
 // Calibrate X Values
 xVal = analogRead(x);
 if(xVal>xMax){
 xMax=xVal;
 }else if (xVal < xMin){
 xMin=xVal;
 }

 // Calibrate Y Values
 yVal = analogRead(y);
 if(yVal>yMax){
 yMax=yVal;
 }else if (yVal < yMin){
 yMin=yVal;
 }

 // Calibrate Z Values
 zVal = analogRead(z);
 if(zVal>zMax){
 zMax=zVal;
 }else if (zVal < zMin){
 zMin=zVal;
 }

 //Delay 10msec between readings
 delay(10);
 }
 
 //End of calibration sequence sound. ARMED.
 buzz(3,40);
 printValues(); //Only useful when connected to computer- using serial monitor.
 calibrated=true;
 
}



//Function used to detect motion. Tolerance variable adjusts the sensitivity of movement detected.
boolean checkMotion(){
 boolean tempB=false;
 xVal = analogRead(x);
 yVal = analogRead(y);
 zVal = analogRead(z);
 
 if(xVal >(xMax+tolerance)||xVal < (xMin-tolerance)){
 tempB=true;
 Serial.print("X Failed = ");
 Serial.println(xVal);
 }
 
 if(yVal >(yMax+tolerance)||yVal < (yMin-tolerance)){
 tempB=true;
 Serial.print("Y Failed = ");
 Serial.println(yVal);
 }
 
 if(zVal >(zMax+tolerance)||zVal < (zMin-tolerance)){
 tempB=true;
 Serial.print("Z Failed = ");
 Serial.println(zVal);
 }
 
 return tempB;
}
 




// Prints the Sensor limits identified during Accelerometer calibration.
// Prints to the Serial monitor.
void printValues(){
 Serial.print("xMin=");
 Serial.print(xMin);
 Serial.print(", xMax=");
 Serial.print(xMax);
 Serial.println();
 
 Serial.print("yMin=");
 Serial.print(yMin);
 Serial.print(", yMax=");
 Serial.print(yMax);
 Serial.println();
 
 Serial.print("zMin=");
 Serial.print(zMin);
 Serial.print(", zMax=");
 Serial.print(zMax);
 Serial.println();
 
 Serial.println("------------------------");
}




//Function used to make the alarm sound, and blink the LED.
void ALARM(){

 //don't check for movement until recalibrated again
 calibrated=false;
 
 // sound the alarm and blink LED
 digitalWrite(ledPin, HIGH);
 buzz(4,20);
 digitalWrite(ledPin, LOW);
}
