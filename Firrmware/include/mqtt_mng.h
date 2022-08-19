#ifndef MQTT_MNG_H_
#define MQTT_MNG_H_

#define BUFFER_MAX_SIZE 100

void mqtt_mng_reconnect();      
void mqtt_mng_init();           
void mqtt_mng_loop();      
void mqtt_mng_disconnect();
void mqtt_mng_callback(char* topic, byte *payload, unsigned int length) ;


#endif /* MQTT_MNG_H_ */