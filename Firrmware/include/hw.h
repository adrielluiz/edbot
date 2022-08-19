#ifndef HW_H_
#define HW_H_

#define PIN_SERVO0  2   // SERVOB 8
#define PIN_SERVO1  4   // SERVOB 6
#define PIN_SERVO2  17  // SERVOB 4
#define PIN_SERVO3  18  // SERVOB 2
#define PIN_GRIPPER 16  // SERVOB 5
#define PIN_LED1 33     //PROGRAM MODE (HIGH->RUN, LOW->CONFIG)
#define PIN_LED2 26     //STATUS MQTT CONNECT
#define PIN_LED3 14     //STATUS WIFI STA 
#define PIN_BTN  35
#define DEBOUNCE_TIME 50 //ms
#define LED_HIGH LOW
#define LED_LOW  HIGH
#define DELAY_SERVO_MS 10
#define DELAY_INIT_SERVO_MS 200

typedef struct servo_s
{
  int    pin;
  int    max_pos;
  int    min_pos;
  int    init_pos;
} servo_t;

void hw_set_btn_interrupt(void);
void hw_gpio_init(void);
int hw_read_digital_pin(uint8_t pin);
void hw_write_digital_pin(uint8_t pin, uint8_t value);
void hw_delay_ms(uint16_t time);
void hw_blink_led(uint8_t led_pin);
void hw_init_servos(void);
void hw_set_servo_position(uint8_t servo, uint8_t pos);
void hw_servos_config(void);
void hw_set_servos_init_position(void);

#endif /* HW_H_ */