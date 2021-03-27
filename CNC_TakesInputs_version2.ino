

/* Program to run the motors for CNC
 *  Will use commands that user inputs to direct motors.
 *  roughly 250 steps = 1 inch linear motoion with a 400 microstep setting on drivers
 */
#include <AccelStepper.h>

int desiredDistance = 0; //distance in steps or inches, user input
int desiredSpeed = 0; //delay between two steps used with maxspeed, user input
int desiredAccel = 0; //acceleration value from computer
char Command; //character for commands

/* Create Switch Case with Right/Left/Forward/Back
   'C' : Prints all the commands and their functions. 
    'F' : Moves Y-direction Motors Forward relative to current position, (CCW) for left and (CW) for right.
    'f' : Moves Y-direction Motors forward Absolute to their 'Home' positions. 
    'B' : Moves Y-direction Motors Backwards relative to current position, (CW) for left and (CCW) for right.
    'b' : Moves Motors Backwards an Absolute distance from their 'Home' positions. 
    'R' : Moves X-direction Motor Right (CW) relative to current position.
    'r' : Moves motor right (CW) an Absolute distance from 'Home' position.
    'L' : Moves X-direction Motor Left (CCW) relative to current position. 
    'l' : Moves motor left (CCW) an Absolute distance from 'Home' position. 
    'W' : Shows Where the motors are currently at (Location) 
    'U' : Updates the current position and resets it as the new 0 (Home) position.
    'H' : Homing, returns all motors to their 'Home' or 0 positions.
    'A' : Updates motor's Acceleration.
    'S' : Stops all Motors Immediately.
 */
int userInches = 0;
int desiredDirection = 1;         // +1 for positive direction (Right for X, forward for y), -1 for Negative direction (Left for X, back for y) 
bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag
boolean setdir = LOW;       //Set Direction. Toggling this reverses the motor mid command (Limit Switches)

// const byte interruptPin = 2; //pin for button to use attachInterrupt() (Limit Switch 1)
// const byte interruptPin2 = 3;


// direction Digital 9 (CCW), pulses Digital 8 (CLK)
AccelStepper stepper(1, 7, 6);       //y-direction on left side
AccelStepper stepper2(1, 11, 10);    //y-direction on right side
AccelStepper stepper3(1, 13, 12);   //x-direction

void revMotor ()       //Interrupt Handler, inverts the boolean variable setdir and reverses direction.
{     
  setdir = !setdir;
}

void setup()
{
  Serial.begin(9600);                               //define baud rate
  Serial.println("Testing CNC system");            //print a message
  Serial.println("press 'C' for a list of commands.");
  Serial.println("Enter Command, distance(inches), speed (RPM).");

  // Default values for maximum speed and acceleration
  Serial.println("Default speed: 1000 steps/s, default Acceleration: 800 steps/s^2.");
  stepper.setMaxSpeed(1000);                      //SPEED = Steps / second
  stepper.setAcceleration(800);                  //ACCELERATION = Steps /(second)^2
  stepper.disableOutputs();               //disable outputs, so the motor is not getting warm (no current)
  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(800);
  stepper2.disableOutputs();
  stepper3.setMaxSpeed(1000);       //x-direction default
  stepper3.setAcceleration(800);
  stepper3.disableOutputs();
}
void loop()   //Constantly loops these functions
{
  checkSerial();      //check serial port for new commands
  runPrograms();      //method to handle the motor 
}

void runPrograms()  //Various actions for motors
{
  if (runallowed == true)
  {
      stepper.enableOutputs();         //Enable pins
      stepper2.enableOutputs();       
      stepper3.enableOutputs();      
      stepper.run();              //Step the motors 1 step at each loop
      stepper2.run();           
      stepper3.run();           
  }
  else                      //Enters this if the runallowed variable is 'FALSE' then do nothing
   {
      disablePower();                  //Disables Power to output pins       
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

    if (newData == true)          //Only enters switch case if new command is entered
    {
      switch(Command)         //Checks Command Variable
      {
        case 'F':     //Uses the .move() function of AccelStepper Library, so it moves relatively to current position
        {
          //Go Forward, Example: F 20 500 => 20 inches and 500 steps/s
          //Moves X steps from current position of stepper motor.
          
          runallowed = true;                       //allow running
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;      // Converts Inches to steps for motors. Is roughly 250Steps/1-inch
          desiredSpeed = Serial.parseFloat();      //grabs value for speed in RPM
          desiredDirection = 1;
          Serial.println("Moving Forward \n");
        
          stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
          stepper2.setMaxSpeed(desiredSpeed);     
          stepper.move(desiredDistance);        //CCW for Left Y-direciton motor
          stepper2.move(-desiredDistance);         //CW for Right Y-direction motor
          break;
        }
  
        case 'B':   //Uses the .move() function to move backwards relatively to current position
        {
          //Go Backwards
          runallowed = true;                       //allow running
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;       //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();         //grabs value for speed
          desiredDirection = -1;
          Serial.println("Moving backwards \n");
          
          stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
          stepper2.setMaxSpeed(desiredSpeed);     
          stepper.move(-desiredDistance);         //CW for Left Y-direction motor (Check if i need to switch these around)
          stepper2.move(desiredDistance);         //CCW for right Y-direction motor
          break;
        }
        
        case 'R':   //Move right relative to current position (X-direction)
        {
          //Move Right
          userInches = Serial.parseFloat();        // Grabs Inches that User inputs
          desiredDistance = userInches * 250;      //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();      //grabs value for speed
          desiredDirection = -1;                  //CCW
          Serial.println("Moving Right \n");
          moveRelative();                       //Runs function
          break;
        }
        
        case 'L':
        {
          //Move left
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;       //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();       //grabs value for speed
          desiredDirection = 1;                     //CW
          Serial.println("Moving Left \n");
          moveRelative();
          break;
        }
  
        case 'f':     //Uses the .moveTo() function of AccelStepper Library, so it moves absolute to position
        {
          //Go Forward, Example: f20 500 => moves to position which is located +20 inches away from 0
          //Moves X steps from current position of stepper motor.
          
          runallowed = true;                       //allow running
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;      // Converts Inches to steps for motors. Is roughly 250Steps/1-inch
          desiredSpeed = Serial.parseFloat();      //grabs value for speed in RPM
          desiredDirection = 1;
          Serial.println("Moving Forward to Absolute Position (+). \n");
          
          stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
          stepper2.setMaxSpeed(desiredSpeed);     
          stepper.moveTo(desiredDistance);        //CCW for Left Y-direciton motor
          stepper2.moveTo(-desiredDistance);         //CW for Right Y-direction motor
          break;
        }
  
        case 'b':   //Uses the .moveTo() function to move backwards absolute to position
        {
          //Go Backwards
          runallowed = true;                       //allow running
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;       //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();         //grabs value for speed
          desiredDirection = -1;
          Serial.println("Moving backwards Absolute (-). \n");
          
          stepper.setMaxSpeed(desiredSpeed);      //Set Speed for both Y motors
          stepper2.setMaxSpeed(desiredSpeed);     
          stepper.moveTo(-desiredDistance);         //CW for Left Y-direction motor (Check if i need to switch these around)
          stepper2.moveTo(desiredDistance);         //CCW for right Y-direction motor
          break;
        }
  
        case 'l':   
        {
          //Move left Absolute to Position(0)
          userInches = Serial.parseFloat();         // Grabs Inches that User inputs
          desiredDistance = userInches * 250;       //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();         //grabs value for speed
          desiredDirection = 1;
          Serial.println("Moving Left Absolute (-). \n");
          moveAbsolute();
          break;
        }
  
        case 'r':   //Move right Absolute to position (X-direction)
        {
          //Move Right
          userInches = Serial.parseFloat();        // Grabs Inches that User inputs
          desiredDistance = userInches * 250;      //Converts to Steps for functions
          desiredSpeed = Serial.parseFloat();      //grabs value for speed
          desiredDirection = -1;
          Serial.println("Moving Right \n");
          moveAbsolute();                       //Runs function
          break;
        }
       
        case 'S':   //Stops All Motors
        {
          stopMotors();
          break;
        }
        
        case 'A':    //Updates Acceleration
        {
          runallowed = false;                 //still keeps running disabled, only updates variable.
          disablePower();                  //Disables Power to output pins
          desiredAccel = Serial.parseFloat();       //Grabs user input value for acceleration from Serial port
          stepper.setAcceleration(desiredAccel);
          stepper2.setAcceleration(desiredAccel);
          stepper3.setAcceleration(desiredAccel);
          Serial.print("Acceleration for all motors Updated to: ");       //Confirmation
          Serial.println(desiredAccel);
          break;
        }
  
        case 'W':   //Where are motors current Location
        {
          runallowed = false;
          disablePower();                  //Disables Power to output pins
          Serial.print("Current Location of the X-direction Motor (inches): ");
          Serial.println(stepper3.currentPosition() /250);        //Prints the current postion. 
                                                              //Function returns in steps change to inches (1"/250 steps)
          
          Serial.print("Current Location of the Left-most Motor (inches): ");
          Serial.println(stepper.currentPosition() /250);
          
          Serial.print("Current Location of the Right-most Motor (inches): ");
          Serial.println(stepper2.currentPosition() /250);
          break;
        }
  
        case 'U':   //Update Motors position. Resets their "Home" value.
        {
          runallowed = false;
          disablePower();                  //Disables Power to output pins
  
          stepper.setCurrentPosition(0);    //Resets Current postion to a new "Home".
          stepper2.setCurrentPosition(0);   //Now if goHome() function is called it will return to this position
          stepper3.setCurrentPosition(0);
          
          Serial.print("Current position X-direction Motor (Middle) is now: ");
          Serial.println(stepper3.currentPosition());
          
          Serial.print("Current position Left-most Motor is now: ");
          Serial.println(stepper.currentPosition());
          
          Serial.print("Current position Right-most Motor is now: ");
          Serial.println(stepper2.currentPosition());
          break;
        }
  
        case 'H':     // Calls the goHome function and returns Motors to designated positions.
        {
          runallowed = true;
          Serial.println("Returning Home");
          goHome();     //Runs function
          break;
        }
        
        case 'C':       // List of Commands
        {
          printCommands(); //Print the commands for controlling the motor
          break;
        }
        
        default:
        {
          Serial.println("NA");
          break;
        }
        
      }
  }
  
    newData = false;
}

void disablePower()
{
  stepper.disableOutputs();        //Disables Power
  stepper2.disableOutputs();
  stepper3.disableOutputs();
}

void stopMotors()    //Stop motors, disable outputs
{
        stepper.stop();                 //Stops motors.
        stepper2.stop();
        stepper3.stop();
        disablePower();                  //Disables Power to output pins
        Serial.println("Stopped.");      //print action
        runallowed = false;              //Disables running
}

void goHome()
{  
    if (stepper.currentPosition() == 0 && stepper2.currentPosition() == 0 && stepper3.currentPosition() == 0)
    {
        Serial.println("We are at the home position.");
        disablePower();                  //Disables Power to output pins
    }
    else
    {
        stepper.setMaxSpeed(400);       //set speed manually to 400. In this project 400 is 400 step/sec = 1 rev/sec.
        stepper2.setMaxSpeed(400); 
        stepper3.setMaxSpeed(400); 
        stepper.moveTo(0);              //set absolute distance to move
        stepper2.moveTo(0);
        stepper3.moveTo(0);
    }
}

void moveRelative()
{
    //We move X steps from the current position of the stepper motor in a given direction.
    //The direction is determined by the direction variable (+1 or -1)
   
    runallowed = true;                      //allow running - this allows entering the runPrograms() function.
    stepper3.setMaxSpeed(desiredSpeed);                  //set speed
    stepper3.move(desiredDirection * desiredDistance);       //set relative distance and direction
}

void moveAbsolute()
{
    //move to an absolute position. The AccelStepper library keeps track of the position.
    //The direction is determined by the multiplier (+1 or -1)
    //Why do we need negative numbers? - If Zero position is set to Middle of V-rail.
 
    runallowed = true; //allow running - this allows entering the RunTheMotor() function.
    stepper3.setMaxSpeed(desiredSpeed); //set speed          //Left or right is only Motor 3 (X-direction)
    stepper3.moveTo(desiredDirection * desiredDistance); //set relative distance   
}

void printCommands()
{
  //Printing the commands 
    Serial.println(" 'C' : Prints all the commands and their functions. ");
    Serial.println(" 'F' : Moves Y-direction Motors Forward relative to current position, (CCW) for left and (CW) for right. ");
    Serial.println(" 'f' : Moves Y-direction Motors forward Absolute to their 'Home' positions. ");
    Serial.println(" 'B' : Moves Y-direction Motors Backwards relative to current position, (CW) for left and (CCW) for right. ");
    Serial.println(" 'b' : Moves Motors Backwards an Absolute distance from their 'Home' positions. ");
    Serial.println(" 'R' : Moves X-direction Motor Right (CW) relative to current position. "); 
    Serial.println(" 'r' : Moves motor right (CW) an Absolute distance from 'Home' position. ");
    Serial.println(" 'L' : Moves X-direction Motor Left (CCW) relative to current position. ");
    Serial.println(" 'l' : Moves motor left (CCW) an Absolute distance from 'Home' position. ");
    Serial.println(" 'W' : Shows Where the motors are currently at (Location) ");  
    Serial.println(" 'U' : Updates the current position and resets it as the new 0 (Home) position. ");
    Serial.println(" 'H' : Homing, returns all motors to their 'Home' or 0 positions. ");
    Serial.println(" 'A' : Updates motor's Acceleration. ");
    Serial.println(" 'S' : Stops all Motors Immediately. ");
}
