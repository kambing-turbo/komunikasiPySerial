#define LED_pin 9
#define LED_error_pin 8

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_pin, OUTPUT);
  pinMode(LED_error_pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //String msg = "STATIC";
  if (Serial.available() > 0) {
    String msg = Serial.readString();
    if (msg == "ON") {
      digitalWrite(LED_pin, HIGH);
      Serial.println("on");
    }
    else if (msg == "OFF") {
      digitalWrite(LED_pin, LOW);
      Serial.println("off ");
    }

    else {
      digitalWrite(LED_error_pin, HIGH);
      delay(100);
      digitalWrite(LED_error_pin, LOW);
    }
  }
}
