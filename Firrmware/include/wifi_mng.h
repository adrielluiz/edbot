#ifndef WIFI_MNG_H_
#define WIFI_MNG_H_

#define WIFI_AP_SSID "EdBot_v1"
#define WIFI_AP_PWD  "12345678"

typedef enum wifi_mng_s
{
    WIFI_DISCONNECT = 0,
    WIFI_AP_CONNECT,
    WIFI_STA_CONNECT,
    WIFI_APSTA_CONNECT,
}wifi_mng_t;

uint8_t wifi_mng_connect(void);
void wifi_mng_loop(void);

#endif /* WIFI_MNG_H_ */