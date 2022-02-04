/**
 * P21014 Wearable Bluetooth Module Driver
 * Uses Feather M0 Bluefruit BLE, Adafruit BNO055, and Custom PCB/Mounting
 * Author: Adam Seidman
 */

#include <Adafruit_ATParser.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BLEBattery.h>
#include <Adafruit_BLEEddystone.h>
#include <Adafruit_BLEGatt.h>
#include <Adafruit_BLEMIDI.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BluefruitLE_UART.h>

#include <Adafruit_BLE_UART.h>

#include <Arduino.h>
#include <SPI.h>
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include "BluefruitConfig.h"
#include "ShotTrainer.h"

#if SOFTWARE_SERIAL_AVAILABLE
#include <SoftwareSerial.h>
#endif

// Bluetooth Object
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

// IMU Object
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void error(const __FlashStringHelper*err) {
  Serial.println(err);
  while (1);
}

char _buffer[3];
long last_time = 0;
sensors_event_t event;
bool is_sending = false;

void setup(void)
{
  while (!Serial);
  delay(500);

  Serial.begin(BAUD_RATE);
  Serial.println(F("Basketball Shot Trainer Initialization..."));
  Serial.println(F("---------------------------------------"));

  configure_imu();
  configure_bluetooth();

  wait_for_connection();
  last_time = millis();
}

void loop(void)
{
  if (!ble.isConnected()) {
    Serial.println("Lost Bluetooth Connection.");
    wait_for_connection();
  }

  if (is_sending && millis() >= (last_time + WAIT_TIME)) {
    bno.getEvent(&event);

    send_data(event.acceleration.x, ACCEL_X);
    send_data(event.acceleration.y, ACCEL_Y);
    send_data(event.acceleration.z, ACCEL_Z);

    send_data(event.orientation.x, GYRO_X);
    send_data(event.orientation.y, GYRO_Y);
    send_data(event.orientation.z, GYRO_Z);

    last_time = millis();
  }

  handle_incoming();
}

void send_data(float raw_data, uint8_t data_type)
{
  ble.print(TX_COMMAND);

  uint16_t data = (uint16_t)(raw_data * 32.0);

  _buffer[0] = (char)(data_type);
  _buffer[1] = (char)(((uint8_t)(data >> NUM_SHIFTED_BITS)) & DATA_BYTE_MASK);
  _buffer[2] = (char)(((uint8_t)(data & DATA_MASK)) & DATA_BYTE_MASK);

  ble.println(_buffer);

  // check response stastus
  if (! ble.waitForOK() ) {
    Serial.println(F("Failed to send a packet.\n\r"));
  }
}

void handle_incoming(void)
{
  // Check for incoming characters from Bluefruit
  ble.println(RX_COMMAND);
  ble.readline();
  if (strcmp(ble.buffer, "OK") == 0) {
    // no data
    return;
  }
  // Some data was found, its in the buffer

  char rec = ble.buffer[0];
  if (rec == 'a')
  {
    is_sending = true;
    Serial.println("Start Data Requested");
  }
  else if (rec == 'b')
  {
    is_sending = false;
    Serial.println("Stop Data Requested");
  }

  ble.waitForOK();
}

void configure_imu(void)
{
  Serial.print(F("Initializing the BNO055 IMU module: "));

  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1)
      ;
  }

  delay(1000);

  bno.setExtCrystalUse(true);

  Serial.println(F("OK!\n\r"));
}

void configure_bluetooth(void)
{
  /* Initialise the module */
  Serial.print(F("Initializing the Bluefruit LE module: "));

  if ( !ble.begin(VERBOSE_MODE) )
  {
    error(F("Couldn't find Bluefruit, make sure it's in Command mode & check wiring?"));
  }
  Serial.println( F("OK!") );


  /* Disable command echo from Bluefruit */
  ble.echo(false);

  if ( FACTORYRESET_ENABLE )
  {
    /* Perform a factory reset to make sure everything is in a known state */
    Serial.print(F("Performing a factory reset: "));
    if ( ! ble.factoryReset() ) {
      error(F("Couldn't factory reset"));
    } else {
      Serial.println(F("OK!\n\r"));
    }
  }

  Serial.println("Requesting Bluefruit info:");
  /* Print Bluefruit information */
  ble.info();

  ble.verbose(false);  // debug info is a little annoying after this point!

  // Set Device Name
  ble.println(DEVICE_NAME_COMMAND);
}

void wait_for_connection(void)
{
  Serial.println("\n\rWaiting for connection...");

  /* Wait for connection */
  while (! ble.isConnected()) {
    delay(500);
  }

  Serial.println("Connected!\n\r");
}
