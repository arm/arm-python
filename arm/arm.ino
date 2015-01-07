#include <Servo.h>

Servo pinchServo;
Servo wristServo;
Servo elbowServo;
Servo shoulderServoLeft;
Servo shoulderServoRight;
Servo twistServo;


int numServos = 6;
int pinch = 160;
int wrist = 90;
int elbow = 30;
int shoulderL = 60;
int shoulderR = 180 - 66;
int twist = 95;
int smoothness = 3; //change this for smoothness and speed of servos     added for less twitch in initialization

void setup() {
  Serial.begin(9600);

  pinchServo.attach(13);
  wristServo.attach(12);
  elbowServo.attach(11);
  shoulderServoLeft.attach(10);
  shoulderServoRight.attach(9);
  twistServo.attach(8);

  pinchServo.write(pinch);
  wristServo.write(wrist);
  elbowServo.write(elbow);
  shoulderServoLeft.write(shoulderL);
  shoulderServoRight.write(shoulderR);
  twistServo.write(twist);
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
        if(data[0]>pinch+smoothness){                 //can be shortened    added for smoothness
          pinchServo.write(pinch+smoothness);
          pinch = pinch+smoothness;
        }
        else if(data[0]<pinch-smoothness){
          pinchServo.write(pinch-smoothness);
          pinch = pinch-smoothness;
        }
        else{
          pinchServo.write(pinch);
        }
        if(data[1]>wrist+smoothness){
          wristServo.write(wrist+smoothness);
          wrist = wrist+smoothness;
        }
        else if(data[1]<wrist-smoothness){
          wristServo.write(wrist-smoothness);
          wrist = wrist-smoothness;
        }
        else{
          wristServo.write(wrist);
        }
        if(data[2]>twist+smoothness){
          twistServo.write(twist+smoothness);
          twist = twist+smoothness;
        }
        else if(data[2]<twist-smoothness){
          twistServo.write(twist-smoothness);
          twist = twist-smoothness;
        }
        else{
          twistServo.write(twist);
        }
        if(data[3]>elbow+smoothness){
          elbowServo.write(elbow+smoothness);
          elbow = elbow+smoothness;
        }
        else if(data[3]<elbow-smoothness){
          elbowServo.write(elbow-smoothness);
          elbow = elbow-smoothness;
        }
        else{
          elbowServo.write(elbow);
        }
        if(data[4]>shoulderL+smoothness){
          shoulderServoLeft.write(shoulderL+smoothness);
          shoulderL = shoulderL+smoothness;
        }
        else if(data[4]<shoulderL-smoothness){
          shoulderServoLeft.write(shoulderL-smoothness);
          shoulderL = shoulderL-smoothness;
        }
        else{
          shoulderServoLeft.write(shoulderL);
        }
        if(data[5]>shoulderR+smoothness){
          shoulderServoRight.write(shoulderR+smoothness);
          shoulderR = shoulderR+smoothness;
        }
        else if(data[5]<shoulderR-smoothness){
          shoulderServoRight.write(shoulderR-smoothness);
          shoulderR = shoulderR-smoothness;
        }
        else{
          shoulderServoRight.write(shoulderR);
        }
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
