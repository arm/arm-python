#include <Servo.h>

Servo pinchServo;
Servo wristServo;

int numServos = 2;

void setup() {
  Serial.begin(9600);

  pinchServo.attach(13);
  wristServo.attach(12);

  pinchServo.write(160);
  wristServo.write(90);
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
