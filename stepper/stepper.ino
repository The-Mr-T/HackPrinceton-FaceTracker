#include <ArduinoJson.h>

#include <Stepper.h>
#include "include/ArduinoJson.h"

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// change this to the number of steps on your motor // full rotation --> 32*64 = 2048
const int stepsPerRevolution = 64;

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it is
// attached to

Stepper Xstepper(stepsPerRevolution, 8, 10, 9, 11);
Stepper Ystepper(stepsPerRevolution, 2, 5, 3, 6);

// the previous reading from the analog input

void setup() {
  Serial.begin(9600);
  // set speeds at 120 rpm:
  Xstepper.setSpeed(120);
  Ystepper.setSpeed(120);
  // initialize the serial port:
  inputString.reserve(200);
}
//
// Step 1: Reserve memory space
//
StaticJsonBuffer<200> jsonBuffer;


void loop() {

  //Xstepper.step(1*stepsPerRevolution); delay(1000);
  if (stringComplete) {
    //Serial.print(inputString);
    unsigned char buff[30];
    inputString.getBytes(buff, 30);
    //
    // Step 2: Deserialize the JSON string
    //
    JsonObject& root = jsonBuffer.parseObject(buff);

    if (!root.success())
    {
      Serial.println("parseObject() failed");
    }
    else
    {
      int x_offset = root["X"];
      int y_offset = root["Y"];
      Serial.print("Received coordinates : \r\n");
      Serial.print(x_offset);
      Serial.print("\r\n");
      Serial.print(y_offset);
      Serial.print("\r\n");
      Ystepper.step((x_offset/240)*stepsPerRevolution);
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
  
//  if(Serial.read() == 1)
//  while(x_position < UART_in_x) { }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

