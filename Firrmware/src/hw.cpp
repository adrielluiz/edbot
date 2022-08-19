#include <Arduino.h>
#include <ESP32Servo.h>
#include "hw.h"
#include "app.h"

Servo myservo[5];
servo_t servo_motor[5];

void IRAM_ATTR hw_btn_interrupt()
{
    unsigned long timestamp_ultimo_acionamento = 0;

    if ((millis() - timestamp_ultimo_acionamento) >= DEBOUNCE_TIME)
    {   
        if(digitalRead(PIN_BTN) == HIGH)
            app_set_program_mode(MODE_OPERATION);
        else
            app_set_program_mode(MODE_CONFIG);   
             
        timestamp_ultimo_acionamento = millis();
    }
}

void hw_set_btn_interrupt(void)
{
    attachInterrupt(PIN_BTN, hw_btn_interrupt, CHANGE);
}

void hw_gpio_init(void)
{
    pinMode(PIN_BTN, INPUT);

    pinMode(PIN_LED1, OUTPUT);
    pinMode(PIN_LED2, OUTPUT);
    pinMode(PIN_LED3, OUTPUT);

    digitalWrite(PIN_LED1, LED_LOW);
    digitalWrite(PIN_LED2, LED_LOW);
    digitalWrite(PIN_LED3, LED_LOW);

    hw_set_btn_interrupt();

    hw_init_servos();    
}

int hw_read_digital_pin(uint8_t pin)
{
    return digitalRead(pin);
}

void hw_write_digital_pin(uint8_t pin, uint8_t value)
{
    digitalWrite(pin, value);
}

void hw_delay_ms(uint16_t time)
{
    delay(time);
}

void hw_blink_led(uint8_t led_pin)
{
    hw_write_digital_pin(led_pin, LED_LOW);
    delay(20);
    hw_write_digital_pin(led_pin, LED_HIGH);
}

void hw_init_servos(void)
{
    hw_servos_config();

	ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	
	myservo[0].setPeriodHertz(50);    
	myservo[0].attach(servo_motor[0].pin, 500, 2400); 

	myservo[1].setPeriodHertz(50);    
	myservo[1].attach(servo_motor[1].pin, 500, 2400); 

	myservo[2].setPeriodHertz(50);    
	myservo[2].attach(servo_motor[2].pin, 500, 2400); 

	myservo[3].setPeriodHertz(50);    
	myservo[3].attach(servo_motor[3].pin, 500, 2400); 

	myservo[4].setPeriodHertz(50);    
	myservo[4].attach(servo_motor[4].pin, 500, 2400);    
}

void hw_set_servo_position(uint8_t servo, uint8_t pos)
{
    uint16_t last_pos = myservo[servo].read();

    if((servo >= 0) && (servo <= 4))
    {
        if((pos >= servo_motor[servo].min_pos) && (pos <= servo_motor[servo].max_pos))
        {
            if(last_pos < pos)
            {
                for (uint8_t p = last_pos; p < pos; p++)
                {
                    myservo[servo].write(p);
                    delay(DELAY_SERVO_MS);
                }
            }
            else if(last_pos > pos)
            {
                for (uint8_t p = last_pos; p > pos; p--)
                {
                    myservo[servo].write(p);
                    delay(DELAY_SERVO_MS);
                }                
            }
        }            

    }
        
}

void hw_servos_config(void)
{
    servo_motor[0].pin = PIN_SERVO0;
    servo_motor[0].min_pos = 0;
    servo_motor[0].max_pos = 180;
    servo_motor[0].init_pos = 90;

    servo_motor[1].pin = PIN_SERVO1;
    servo_motor[1].min_pos = 70;
    servo_motor[1].max_pos = 120;
    servo_motor[1].init_pos = 105;

    servo_motor[2].pin = PIN_SERVO2;
    servo_motor[2].min_pos = 75;
    servo_motor[2].max_pos = 135;
    servo_motor[2].init_pos = 120;

    servo_motor[3].pin = PIN_SERVO3;
    servo_motor[3].min_pos = 0;
    servo_motor[3].max_pos = 110;
    servo_motor[3].init_pos = 40;

    servo_motor[4].pin = PIN_GRIPPER;
    servo_motor[4].min_pos = 80;
    servo_motor[4].max_pos = 140;
    servo_motor[4].init_pos = 140;
}

void hw_set_servos_init_position(void)
{
    myservo[4].write(servo_motor[4].init_pos);
    delay(DELAY_INIT_SERVO_MS);

    myservo[3].write(servo_motor[3].init_pos);
    delay(DELAY_INIT_SERVO_MS);

    myservo[2].write(servo_motor[2].init_pos);
    delay(DELAY_INIT_SERVO_MS);

    myservo[1].write(servo_motor[1].init_pos);
    delay(DELAY_INIT_SERVO_MS);

    myservo[0].write(servo_motor[0].init_pos);
    delay(DELAY_INIT_SERVO_MS);
}
