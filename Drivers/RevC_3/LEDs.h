#ifndef __LEDs__
#define __LEDs__

#define RED_PIN     6
#define GREEN_PIN   9
#define BLUE_PIN    10

#define COLOR_MSK   (0x1)
#define RED_BIT     (0)
#define GREEN_BIT   (1)
#define BLUE_BIT    (2)

#define RED         (COLOR_MSK << RED_BIT)
#define GREEN       (COLOR_MSK << GREEN_BIT)
#define BLUE        (COLOR_MSK << BLUE_BIT)

#define YELLOW      (RED | GREEN)
#define TEAL        (GREEN | BLUE)
#define PURPLE      (RED | BLUE)
#define WHITE       (RED | GREEN | BLUE)
#define OFF         (0x0)

#define INIT        (PURPLE)
#define BLINK       (PURPLE)
#define NORMAL      (OFF)
#define ERR         (RED)
#define AWAIT_CONN  (BLUE)

#endif
