// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#define DHTPIN 11     // what pin we're connected to

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11 
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); 
  Serial.print("DHTxx test!");
}
String serial_command(){
  String cmd="";
  while(Serial.available()){
    cmd+=char(Serial.read());
    //Serial.print("Sam: cmd = ");
    //Serial.write(cmd); 
    delay(2);
  }
   
   
   //Serial.flush();	
  return cmd;
}
void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  //String cmd=serial_command();
  
  //if(cmd=="11"){
  //Serial.flush();
  String cmd="";
  while(1){
    if(Serial.available()){
      cmd+=char(Serial.read());
      delay(2);
      
}else{break;}  
  }
  if(cmd=="PING"){
  Serial.print("OK");
}
  //delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  //lcd.clear();
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {
    Serial.print("Humidity: "); 
    Serial.print(h);
    Serial.print(" %\t");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.println(" *C");
  }
  delay(150);
}

