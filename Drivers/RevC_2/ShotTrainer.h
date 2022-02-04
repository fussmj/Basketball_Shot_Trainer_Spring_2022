#ifndef  __shot_trainer__
#define  __shot_trainer__

// Adafruit Bluetooth Includes
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

// BNO055 Sensor Includes
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// BLEUART PROPERTIES
#define  FACTORYRESET_ENABLE          1

// BLE COMMANDS
#define  TX_COMMAND                   "AT+BLEUARTTX="
#define  RX_COMMAND                   "AT+BLEUARTRX"
#define  DEVICE_NAME_COMMAND          "AT+GAPDEVNAME=Shot Trainer-Arm Module 1"

// BYTE HEADER INFORMATION
#define  FULL_BYTE                    (0xFF)
#define  NUM_SHIFTED_BITS             (7)
#define  BYTE_TYPE_POS                (1 << NUM_SHIFTED_BITS)
#define  HEADER_BYTE_MASK             (BYTE_TYPE_POS)
#define  DATA_BYTE_MASK               (~BYTE_TYPE_POS)
#define  DATA_MASK                    (0x007F)

// BYTE TYPE INFORMATION
#define  START_CMD                    'a'
#define  STOP_CMD                     'b'
#define  GYRO_X                       (HEADER_BYTE_MASK | 0x1)
#define  GYRO_Y                       (HEADER_BYTE_MASK | 0x2)
#define  GYRO_Z                       (HEADER_BYTE_MASK | 0x3)

// HARDWARE UART SETTINGS
#ifdef Serial1    // this makes it not complain on compilation if there's no Serial1
  #define BLUEFRUIT_HWSERIAL_NAME     Serial1
#endif

// SHARED SPI SETTINGS
#define BLUEFRUIT_SPI_CS              (8)
#define BLUEFRUIT_SPI_IRQ             (7)
#define BLUEFRUIT_SPI_RST             (4)

// ASSORTED CONSTANTS
#define  BAUD_RATE                    (115200)
#define  PER_SEC                      (5)
#define  WAIT_TIME                    (1000 / PER_SEC)
#define  DATA_FACTOR                  (32.0)
#define  I2C_PORT                     (55)

#endif
