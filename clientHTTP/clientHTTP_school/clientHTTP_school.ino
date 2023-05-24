#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Aaron-LAN";
const char* password = "helpendehand69";
const char* serverUrl = "http://192.168.0.10:5000/queue";

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
            sendData();
            while(!digitalRead(buttonPin)) {
                delay(5);
            }
            sendData();
        }
    }
  }
  else {
    error_blink();
  }
}

void sendData() {
    digitalWrite(ledPin, !digitalRead(buttonPin));
    // create a HTTP client object
    HTTPClient http;
    WiFiClient client;
    String postData = "cid=" + String(cid) + "&button=" + String(!digitalRead(buttonPin));
    http.begin(client,serverUrl); // maak verbinding met server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpCode = http.POST(postData);
    
    if (httpCode < 0) {
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
