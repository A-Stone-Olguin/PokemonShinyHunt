#include <Servo.h>

Servo startServo;
Servo stickServo;
Servo AServo;

const int START_SERVO_PIN = 9;
const int STICK_SERVO_PIN = 10;
const int A_SERVO_PIN = 11;

const int START_REST_ANGLE = 90;
const int START_PUSH_ANGLE = 45;

const int STICK_REST_ANGLE = 90;
const int STICK_PUSH_ANGLE = 45;

const int A_REST_ANGLE = 90;
const int A_PUSH_ANGLE = 45;


void setup() {
  Serial.begin(115200);

  startServo.attach(START_SERVO_PIN);
  stickServo.attach(STICK_SERVO_PIN);
  aServo.attach(A_SERVO_PIN);
  
  startServo.write(START_REST_ANGLE);
  stickServo.write(STICK_REST_ANGLE);
  aServo.write(A_REST_ANGLE);

  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    String command = readStringUntil('\n');
    command.trim();

    handleCommand(command);
  }
}

void handleCommand(String command) {
  if (command == "PRESS_START") {
    pressStart();
    return;
  }

  if (command == "PRESS_A") {
    pressA();
    return;
  }

  if (command == "STICK_UP") {
    stickUp();
    return;
  }

  if (command == "STICK_RELEASE") {
    stickRelease();
    return;
  }

  if (command == "PING") {
    Serial.println("PONG");
    return;
  }

  Serial.print("ERROR UNKOWN COMMAND ");
  Serial.println(command);
}

void pressStart() {
  startServo.write(START_PUSH_ANGLE);
  delay(150);
  startServo.write(START_REST_ANGLE);
  Serial.println("OK PRESS_START");
}

void pressA() {
  aServo.write(A_PUSH_ANGLE);
  delay(150);
  aServo.write(A_REST_ANGLE);
  Serial.println("OK PRESS_A");
}

void stickUp() {
  stickServo.write(STICK_PUSH_ANGLE);

  println("OK STICK_UP");
}

void stickRelease() {
  stickServo.write(STICK_REST_ANGLE);

  Serial.println("OK STICK_RELEASE");
}
