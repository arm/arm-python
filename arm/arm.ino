#include <Servo.h>

Servo pinchServo;
Servo wristServo;
Servo twistServo;
Servo shoulderServoLeft;
Servo shoulderServoRight;

int numServos = 5;

void setup() {
  Serial.begin(9600);

  pinchServo.attach(13);
  wristServo.attach(12);
  shoulderServoLeft.attach(10);
  shoulderServoRight.attach(9);
  twistServo.attach(8);

  pinchServo.write(160);
  wristServo.write(90);
  shoulderServoLeft.write(60);
  shoulderServoRight.write(180 -  66);
  twistServo.write(95);
}


boolean reading = false;
int count = 0;

void loop() {
  if (Serial.available()) {
    if (reading) {
      if (Serial.available() >= numServos) {
        byte data[numServos];
        Serial.readBytes(data, numServos);
        reading = false;
        pinchServo.write(data[0]);
        wristServo.write(data[1]);
        twistServo.write(data[2]);
        shoulderServoLeft.write(data[3]);
        shoulderServoRight.write(data[4]);
      }
    }
    else {
      byte first = Serial.read();
      Serial.print("first: ");
      Serial.println(first);

      if (first == 0xff) {
        reading = true;
      }
    }
  }

}
