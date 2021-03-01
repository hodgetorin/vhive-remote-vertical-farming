/* This program bidirectionally communicates with Raspberry Pi.
When the Arduino receives info, the Arduino repeats this info to the Pi.*/

void setup() {
  Serial.begin(9600);
}

/* The Arduino checks if it has received data with Serial.available(). This returns number of bytes received.
The string is ready until the new line character appears. All bytes received until '\n' are converted to String.
If you wish to read one byte at a time, use Serial.read(), then convert bytes into int, String, etc.*/
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
}
