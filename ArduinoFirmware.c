void setup() {
    Serial.begin(115200);
    while (!Serial) {;}
    Serial.println("STARTUP");
  }
  
  void loop() {
    String msg = Serial.readStringUntil('\n');
    if (msg.startsWith("RD")) {
      int pinNum = msg.substring(2,5).toInt();
      Serial.println(analogRead(pinNum));
    }
    else if (msg != "") {
      Serial.print("Heard "+msg+".\n");
    }
  }  