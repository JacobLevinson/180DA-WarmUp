#include <SPI.h>
#include <WiFiNINA.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Initialize WiFi module
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    while (true);
  }

  // Connect to WiFi network
  char ssid[] = "Jacob IPhone";      // Change this to your WiFi network SSID
  char password[] = "wifi1234";  // Change this to your WiFi network password

  int status = WiFi.begin(ssid, password);
  if (status != WL_CONNECTED) {
    Serial.println("Failed to connect to WiFi network!");
    while (true);
  }

  // Wait for WiFi to be ready
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print available WiFi networks
  int numNetworks = WiFi.scanNetworks();
  Serial.println("");
  Serial.println("Available WiFi Networks:");
  for (int i = 0; i < numNetworks; i++) {
    Serial.print("Network ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.println(WiFi.SSID(i));
  }
}

void loop() {
  // Nothing to do in the loop
}
