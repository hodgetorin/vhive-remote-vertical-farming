#include <AccelStepper.h>

long desiredDistance = 0; //distance in steps or mm from the computer
long desiredSpeed = 0; //delay between two steps used with maxspeed, received from the computer
long desiredAccel = 0; //acceleration value from computer
char Command; //character for commands

/* Create Switch Case with Right/Left/Forward/Back
 *  b = back (both Y motors) - needs steps and speed values
 *  f = forward (Both Y motors) - needs steps and speed values
 *  r = right (only x motor) - needs steps and speed values
 *  l = left (Only x motor) - needs steps and speed values
 *  a = set Acceleration - needs Acceleration value
 *  o = goes back to the orgin slowly. Origin should be determined manually - need speed, steps, acceleration etc.
 *  n = stop motors - only needs 'n'
 */
 
bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag
boolean setdir = LOW;  //Set Direction. Toggling this reverses the motor mid command.

const byte interruptPin = 2; //pin for button to use attachInterrupt(); 
const byte interruptPin2 = 3;


// direction Digital 9 (CCW), pulses Digital 8 (CLK)
AccelStepper stepper(1, 13, 12);    //y-direction
AccelStepper stepper2(1, 7, 6);     //y-direction
AccelStepper stepper3(1, 29, 28);   //x-direction

void revMotor ()       //Interrupt Handler, inverts the boolean variable setdir and reverses direction.
{     
  setdir = !setdir;
}

void setup()
{
  pinMode(interruptPin, INPUT_PULLUP);  // internal pullup resistor (debouncing) used to stop
  pinMode(interruptPin2, INPUT_PULLUP); // button used to reverse direction
  
  attachInterrupt(digitalPinToInterrupt(interruptPin), stopMotor, FALLING); 
  attachInterrupt(digitalPinToInterrupt(interruptPin2), revMotor, FALLING);
  //FALLING:make sure switch connects the pin to the GND when it is pressed.
 
  
  Serial.begin(9600);                         //define baud rate
  Serial.println("Testing CNC system");     //print a message

  // Default values for maximum speed and acceleration
  stepper.setMaxSpeed(2000); //SPEED = Steps / second
  stepper.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
  stepper.disableOutputs(); //disable outputs, so the motor is not getting warm (no current)
  
  stepper2.setMaxSpeed(2000);
  stepper2.setAcceleration(1000);
  stepper2.disableOutputs();

  stepper3.setMaxSpeed(2000);       //x-direction default
  stepper3.setAcceleration(1000);
  stepper3.disableOutputs();

}

void loop()
{
  
  checkSerial();      //check serial port for new commands

  runPrograms();      //method to handle the motor 

}

void runPrograms()  //Various actions for motors
{
  if (runallowed == true)
  {
    if (abs(stepper.currentPosition()) < desiredDistance)   
    {
      stepper.enableOutputs();         //Enable pins
      stepper2.enableOutputs();       //**Might need to fix
      stepper3.enableOutputs();      //**Might need to fix
      stepper.run();              //Step the motor 1 step at each loop
      stepper2.run();           //**Might need to fix
      stepper3.run();           //**Might need to fix
    }
    else                          //Enters this if the desired distance is completed
    {
      runallowed = false;             //Stops running 
      stepper.disableOutputs();       //Disables power to pins
      stepper2.disableOutputs();          //**Might need to fix
      stepper3.disableOutputs();          //**Might need to fix
      Serial.print("Position: ");
      Serial.println(stepper.currentPosition());      //Print position -> will show latest relative # of steps
      stepper.setCurrentPosition(0);                 //Resets the position to 0
      Serial.print("Position: ");               
      Serial.println(stepper.currentPosition());    //Prints position and checks if it is 0
    }
    
  }
  
  else            //Enters this if the runallowed variable is 'FALSE' then nothing is done
  {
    return;
  }
}

void checkSerial()      //Function for receiving commands/desired behavior (Switch-case)
{
  if (Serial.available() > 0)     //If something is typed
  {
    Command = Serial.read();      //Reads the command character and assigns it to the variable, command
    newData = true;               //Creates a flag
  }

  if (newData == true)          //Beginning of switch case
  {
    switch(Command)
    {
      case 'f':
      {
        //Go Forward, Example: f 2000 500 - 2000 steps and 500 steps/s
        runallowed = true;                       //allow running
        desiredDistance = Serial.parseFloat();      //Value for steps
        desiredSpeed = Serial.parseFloat();         //grabs value for speed

        Serial.print(desiredDistance);
        Serial.print(desiredSpeed);
        Serial.println("Moving Forward \n");
        stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
        stepper2.setMaxSpeed(desiredSpeed);     
        stepper.move(desiredDistance);          //Clockwise
        stepper2.move(-desiredDistance);         //CCW
        break;
      }

      case 'b':
      {
        //Go Backwards
        runallowed = true;                       //allow running
        desiredDistance = Serial.parseFloat();      //Value for steps
        desiredSpeed = Serial.parseFloat();         //grabs value for speed

        Serial.print(desiredDistance);
        Serial.print(desiredSpeed);
        Serial.println("Moving backwards \n");
        stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
        stepper2.setMaxSpeed(desiredSpeed);     
        stepper.move(-desiredDistance);
        stepper2.move(desiredDistance);
        break;
      }
      case 'r':
      {
        //Move Right
        runallowed = true;                       //allow running
        desiredDistance = Serial.parseFloat();      //Value for steps
        desiredSpeed = Serial.parseFloat();         //grabs value for speed

        Serial.print(desiredDistance);
        Serial.print(desiredSpeed);
        Serial.println("Moving Right \n");
        stepper3.setMaxSpeed(desiredSpeed);      //Set Speed for X motor  
        stepper3.move(desiredDistance);
        break;
      }
      case 'l':
      {
        //Move left
        runallowed = true;                       //allow running
        desiredDistance = Serial.parseFloat();      //Value for steps
        desiredSpeed = Serial.parseFloat();         //grabs value for speed

        Serial.print(desiredDistance);
        Serial.print(desiredSpeed);
        Serial.println("Moving Left \n");
        stepper3.setMaxSpeed(desiredSpeed);      //Set Speed for X motor  
        stepper3.move(-desiredDistance);
        break;
      }
      //STOP
      case 'n':
      {
        //Stops all motors
        runallowed = false;                   //Disables running
        
        stepper.setCurrentPosition(0);        //Reset Position
        stepper2.setCurrentPosition(0);
        stepper3.setCurrentPosition(0);
        Serial.println("STOP ");            //print action
        stepper.stop();                   //Stops motors.
        stepper2.stop();
        stepper3.stop();
        stepper.disableOutputs();         //Disables Power
        stepper2.disableOutputs();
        stepper3.disableOutputs();
        break;
      }
      //Set Acceleration
      case 'a':
      {
        runallowed = false;                 //still keeps running disabled, only updates variable.
        desiredAccel = Serial.parseFloat();
        stepper.setAcceleration(desiredAccel);
        stepper2.setAcceleration(desiredAccel);
        stepper3.setAcceleration(desiredAccel);
        Serial.println("Acceleration Update ");       //Confirmation
        break;
      }
      default:
        Serial.println("NA");
    }
  }
  
    newData = false;
}

  void stopMotor()
  {
    //Stop motors, disable outputs
    runallowed = false;           //Disables running
    stepper.setCurrentPosition(0);        //Reset Position
    stepper2.setCurrentPosition(0);
    stepper3.setCurrentPosition(0);
    Serial.println("STOP ");
    stepper.stop();                   //Stops Motors
    stepper2.stop();
    stepper3.stop();
    stepper.disableOutputs();         //Disables Power
    stepper2.disableOutputs();
    stepper3.disableOutputs();

    Serial.println("Pressed.");       //Feedback for button
  }
