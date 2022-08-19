#include <Arduino.h> //Teste
#include <stdint.h>
#include "app.h"
#include "hw.h"
#include "wifi_mng.h"
#include "mqtt_mng.h"
extern "C" {
#include <buffer.h>
}

operation_mode_t program_mode = MODE_CONFIG;
extern buffer_t cbf;

void app_init(void)
{
    hw_gpio_init();
    hw_set_servos_init_position();
    program_mode = app_get_program_mode();
    wifi_mng_connect();
    mqtt_mng_init();   
}

void app_loop(void)
{
    uint8_t servo_id = 0;
    uint8_t position = 0;

    switch (program_mode)
    {
    case MODE_OPERATION:
        mqtt_mng_loop();
        if(buffer_bytes_available(&cbf) > 0)
        {
            buffer_get(&cbf, &servo_id);
            buffer_get(&cbf, &position);

            hw_set_servo_position(servo_id, position);
        }
        break;
    case MODE_CONFIG:
        wifi_mng_loop();
        break;
    default:
        break;
    }    
    
}

operation_mode_t app_get_program_mode(void)
{
    operation_mode_t init_mode;

    if(hw_read_digital_pin(PIN_BTN) == 1)
    {
        init_mode = MODE_OPERATION;
        hw_write_digital_pin(PIN_LED1, LED_HIGH);
    }        
    else    
    {
        init_mode = MODE_CONFIG;
        hw_write_digital_pin(PIN_LED1, LED_LOW);
    }    

    return init_mode;  
}


void app_set_program_mode(operation_mode_t new_mode)
{
    program_mode = new_mode; 
    hw_write_digital_pin(PIN_LED1, program_mode);
}