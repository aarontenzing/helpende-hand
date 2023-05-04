#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "servertje";
const char* password = "ditismijnservertje";
const char* serverUrl = "http://10.67.128.32:5000/queue";

const int cid = 1;
const int AANT_SEC = 2;

const int buttonPin = 1; // TX 
const int buttonEn = 0; // GPIO0
const int ledPin = 2; // GPIO2

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonEn, OUTPUT);

  digitalWrite(ledPin, LOW);
  digitalWrite(buttonEn, LOW);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    error_blink();
  }
}

void loop() {

  if (WiFi.status() == WL_CONNECTED) {
  // Status van de knop  
    if(!digitalRead(buttonPin)) {
        delay(5);
        if(!digitalRead(buttonPin)) {
            sendData(1);
            while(!digitalRead(buttonPin)) {
                delay(5);
            }
            sendData(2);
            digitalWrite(ledPin, LOW);
        }
    }
  }
  else {
    error_blink();
  }
}

void sendData(int type) {

    // create a HTTP client object
    HTTPClient http;
    WiFiClient client;

    String postData = "cid=" + String(cid);
    http.begin(client,serverUrl); // maak verbinding met server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpCode = http.POST(postData);
    
    if (httpCode == 200 || httpCode == -11) {
      if (type == 1) {
        digitalWrite(ledPin, HIGH);
      }
      if (type == 2) {
        digitalWrite(ledPin, LOW);
      }
    }
    else 
    {
      error_blink();   
    }
    http.end(); // beëindig de HTTP-verbinding  
}

void error_blink() {
  for(int i = 0; i < AANT_SEC; i++) {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
  }
}

