#ifndef  __shot_trainer__
#define  __shot_trainer__

// BLEUART PROPERTIES
#define  FACTORYRESET_ENABLE          1
#define  MINIMUM_FIRMWARE_VERSION     "0.6.6"
#define  MODE_LED_BEHAVIOUR           "MODE"

// BLE COMMANDS
#define  TX_COMMAND                   "AT+BLEUARTTX="
#define  RX_COMMAND                   "AT+BLEUARTRX"

// BYTE HEADER INFORMATION
#define  FULL_BYTE                    (0b11111111)
#define  BYTE_TYPE_POS                (1<<7)
#define  HEADER_BYTE_MASK             (BYTE_TYPE_POS)
#define  DATA_BYTE_MASK               (FULL_BYTE & (~BYTE_TYPE_POS))
#define  DATA_MASK                    (0x007F)

// BYTE TYPE INFORMATION
#define  ACCEL_X                      (HEADER_BYTE_MASK | 0x1)
#define  ACCEL_Y                      (HEADER_BYTE_MASK | 0x2)
#define  ACCEL_Z                      (HEADER_BYTE_MASK | 0x3)
#define  GYRO_X                       (HEADER_BYTE_MASK | 0x4)
#define  GYRO_Y                       (HEADER_BYTE_MASK | 0x5)
#define  GYRO_Z                       (HEADER_BYTE_MASK | 0x6)

// ASSORTED CONSTANTS
#define  NUM_SHIFTED_BITS             (7)
#define  BAUD_RATE                    (115200)
#define  PER_SEC                      (5)
#define  WAIT_TIME                    (1000 / PER_SEC)
#define  DEVICE_NAME_COMMAND          "AT+GAPDEVNAME=Shot Trainer-Arm Module 1"

#endif
