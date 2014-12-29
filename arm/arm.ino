#include <Servo.h>

Servo pinchServo;

int numServos = 1;

void setup() {
  Serial.begin(9600);

  pinchServo.attach(13);
  pinchServo.write(160);
}

void loop() {
  if (Serial.available()) {

    byte first = Serial.read();
    Serial.print("first: ");
    Serial.println(first);

    if (first == 0xff) {
      int count = 0;
      while (count < numServos) {
        if (Serial.available()) {
          int pinch = Serial.read();// - '0';
          //          Serial.print("pinch: ");
          //          Serial.println(pinch);
          count++;
          pinchServo.write(pinch);
        }
      }
    }
  }
  //  delay(5);
}
