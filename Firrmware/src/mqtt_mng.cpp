#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "mqtt_mng.h"
#include "hw.h"
extern "C" {
#include <buffer.h>
}

WiFiClient wifi_mqtt_client;
PubSubClient client_mqtt(wifi_mqtt_client);

const char* mqttBroker = "test.mosquitto.org";
char payload[100];
const char* topic_subscribe = "edbotv1_ufu2022/position/set";

StaticJsonDocument<100> doc;

buffer_t cbf;
static uint8_t cbf_area[BUFFER_MAX_SIZE];

void mqtt_mng_callback(char* topic, byte *payload, unsigned int length) 
{
    uint8_t servo = 0;
    uint8_t pos = 0;

    DeserializationError error = deserializeJson(doc, payload);

    if (!error)
    {
        servo = doc["motor"];
        pos = doc["pos"];

        buffer_put(&cbf, servo);
        buffer_put(&cbf, pos);

        hw_blink_led(PIN_LED2);
    }
}

void mqtt_mng_reconnect()
{    
    while (!client_mqtt.connected())
    {
        if (client_mqtt.connect("EdBotV1"))
        {
           client_mqtt.subscribe(topic_subscribe);
           hw_write_digital_pin(PIN_LED2, LED_HIGH);
        }
        else
        {
            hw_write_digital_pin(PIN_LED2, LED_LOW);
            delay(1000);
        }
    }
}

void mqtt_mng_init()
{
    client_mqtt.setServer(mqttBroker, 1883);
    client_mqtt.setCallback(mqtt_mng_callback);
    buffer_init(&cbf, cbf_area, BUFFER_MAX_SIZE);
}

void mqtt_mng_disconnect()
{
   client_mqtt.disconnect();    
}

void mqtt_mng_loop()
{
    if (!client_mqtt.connected())
    {
        mqtt_mng_reconnect();
    }
    client_mqtt.loop();
}