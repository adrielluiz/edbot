#ifndef APP_H_
#define APP_H_

typedef enum operation_mode_s
{
    MODE_OPERATION = 0,
    MODE_CONFIG,
} operation_mode_t;



void app_init(void);
void app_loop(void);
operation_mode_t app_get_program_mode();
void app_set_program_mode(operation_mode_t new_mode);


#endif /* APP_H_ */