#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "servertje";
const char* password = "ditismijnservertje";
const char* serverUrl = "http://10.67.128.61:5000/queue";

const int cid = 1;
const int AANT_SEC = 2;

const int buttonPin = 1; // TX 
//const int buttonEn = 0; // GPIO0
const int ledPin = 2; // GPIO2

int ButtonState = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  //pinMode(buttonEn, OUTPUT);
  digitalWrite(ledPin, LOW);
  //digitalWrite(buttonEn, LOW);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    error_blink();
  }
  
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {

  // Status van de knop  
  if(!digitalRead(buttonPin)) {
      delay(5);
      if(!digitalRead(buttonPin)) {
          sendData();
          while(!digitalRead(buttonPin)) {
              delay(5);
          }
          sendData();
          digitalWrite(ledPin, LOW);
      }
  }

}

void sendData() {

   // create a HTTP client object
    HTTPClient http;
    WiFiClient client;

    String postData = "cid=" + String(cid);
    http.begin(client,serverUrl); // maak verbinding met server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int responseCode = http.POST(postData);
    Serial.println(responseCode);
    
    if (responseCode > 0) {
      digitalWrite(ledPin, HIGH);
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

