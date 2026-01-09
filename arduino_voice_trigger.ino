/*
 * Arduino UNO Q - Voice Generation Trigger
 * 
 * This sketch runs on the STM32U585 MCU side and communicates with
 * the Linux MPU side to trigger voice generation.
 * 
 * Hardware:
 * - Button on pin 2 to trigger voice output
 * - LED on pin 13 for status indication
 * 
 * Serial Communication:
 * - Sends text commands to Linux side via Serial
 * - Linux Python script listens and generates speech
 */

const int BUTTON_PIN = 2;
const int LED_PIN = 13;

int buttonState = 0;
int lastButtonState = 0;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

int messageIndex = 0;
String messages[] = {
  "Button pressed",
  "Arduino UNO Q voice system ready",
  "Offline voice generation active",
  "System status: operational",
  "Hello from the microcontroller"
};

void setup() {
  // Initialize serial communication with Linux MPU
  Serial.begin(115200);
  
  // Initialize hardware pins
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  // Wait for serial connection
  while (!Serial) {
    delay(100);
  }
  
  // Send startup message
  Serial.println("SPEAK:Arduino voice system initialized");
  
  // Blink LED to indicate ready
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void loop() {
  // Read button with debouncing
  int reading = digitalRead(BUTTON_PIN);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      
      // Button pressed (LOW because of INPUT_PULLUP)
      if (buttonState == LOW) {
        // Turn on LED
        digitalWrite(LED_PIN, HIGH);
        
        // Send message to Linux side for voice synthesis
        Serial.print("SPEAK:");
        Serial.println(messages[messageIndex]);
        
        // Cycle through messages
        messageIndex = (messageIndex + 1) % 5;
        
        delay(500);  // Prevent rapid triggering
        digitalWrite(LED_PIN, LOW);
      }
    }
  }
  
  lastButtonState = reading;
  
  // Check for incoming messages from Linux side
  if (Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');
    
    if (incoming.startsWith("STATUS:")) {
      // LED blink pattern based on status
      if (incoming.indexOf("OK") >= 0) {
        blinkLED(1, 100);
      } else if (incoming.indexOf("ERROR") >= 0) {
        blinkLED(3, 50);
      }
    }
  }
  
  delay(10);
}

void blinkLED(int times, int duration) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(duration);
    digitalWrite(LED_PIN, LOW);
    delay(duration);
  }
}
