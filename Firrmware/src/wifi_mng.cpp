#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>
#include "wifi_mng.h"
#include "hw.h"
#include "index.h"

const char* wifi_network_ssid = "xxxxxx";
const char* wifi_network_password =  "xxxxxxxx";
uint8_t wifi_status = WIFI_DISCONNECT;

WebServer server(80);
String header;
WiFiClient client;

void onJavaScript(void)
{
    server.setContentLength(jquery_min_js_v3_2_1_gz_len);
    server.sendHeader(F("Content-Encoding"), F("gzip"));
    server.send_P(200, "text/javascript", jquery_min_js_v3_2_1_gz, jquery_min_js_v3_2_1_gz_len);
}

uint8_t wifi_mng_connect(void)
{
    uint8_t num_tries = 0;

    WiFi.mode(WIFI_MODE_APSTA);
    
    if(WiFi.softAP(WIFI_AP_SSID, WIFI_AP_PWD) == true)
        wifi_status = WIFI_AP_CONNECT;    
       
    WiFi.begin(wifi_network_ssid, wifi_network_password);

    while ((WiFi.status() != WL_CONNECTED) && (num_tries < 10))
    {
        num_tries++;
        hw_delay_ms(500);
        Serial.println(".");
    }
    
    if(WiFi.status() == WL_CONNECTED)
    {
        hw_write_digital_pin(PIN_LED3, LED_HIGH);

        if(wifi_status == WIFI_AP_CONNECT)
            wifi_status = WIFI_APSTA_CONNECT;
        else    
            wifi_status = WIFI_STA_CONNECT;    
    }
    else
        hw_write_digital_pin(PIN_LED3, LED_LOW);

    /*return javascript jquery */
    server.on("/jquery.min.js", HTTP_GET, onJavaScript);

    server.on("/atualizar", HTTP_GET, []() {
        Serial.println("server.on(/serverIndex)");
        server.sendHeader("Connection", "close");
        server.send(200, "text/html", serverIndex);
    });
    /*handling uploading firmware file */
    server.on("/update", HTTP_POST, []() {
        Serial.println("server.on(/update)");
        server.sendHeader("Connection", "close");
        server.send(200, "text/plain", (Update.hasError()) ? "FAIL" : "OK");
        ESP.restart();
    }, []() {
        HTTPUpload& upload = server.upload();
        if (upload.status == UPLOAD_FILE_START) {
        Serial.printf("Update: %s\n", upload.filename.c_str());
        if (!Update.begin(UPDATE_SIZE_UNKNOWN)) { //start with max available size
            Update.printError(Serial);
        }
        } else if (upload.status == UPLOAD_FILE_WRITE) {
        /* flashing firmware to ESP*/
        if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
            Update.printError(Serial);
        }
        } else if (upload.status == UPLOAD_FILE_END) {
        if (Update.end(true)) { //true to set the size to the current progress
            Serial.printf("Update Success: %u\nRebooting...\n", upload.totalSize);       
        } else {
            Update.printError(Serial);
            
        }
        }
    });
    server.begin();
    return wifi_status;
}

void wifi_mng_loop(void)
{
    server.handleClient();
}

void wifi_mng_disconnect()
{
  WiFi.softAPdisconnect();
  WiFi.disconnect();
}
