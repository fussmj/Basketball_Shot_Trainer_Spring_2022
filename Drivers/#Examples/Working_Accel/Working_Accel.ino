#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <SPI.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup()
{
  Serial.begin(9600);
  Serial.println("Acceleration Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1)
      ;
  }

  delay(1000);
    
  bno.setExtCrystalUse(true);
  Serial.println("Acceleration Sensor Test"); Serial.println("");
}

void loop()
{
  // put your main code here, to run repeatedly:
  clear_screen();
  /*Get a new sensor event */
  sensors_event_t event; 
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("X: ");
  Serial.println(event.acceleration.x * 32, 4);
  Serial.print("Y: ");
  Serial.println(event.acceleration.y * 32, 4);
  Serial.print("Z: ");
  Serial.println(event.acceleration.z * 32, 4);
  
  delay(100);
}

void clear_screen()
{
  Serial.print("\033[2J");
  Serial.print("\033[0;0H");
}
